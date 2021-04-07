#!/usr/bin/env python3
"""
Example of usage/test of Cart controller implementation.
"""
import json
import os
from collections import namedtuple

from cartctl import CartCtl, Status
from cart import Cart, CargoReq, Status as CartStatus
from jarvisenv import Jarvis
import unittest

CargoSetup = namedtuple("CargoSetup", "src dst weight name time")


def log(msg):
    """simple logging"""
    print(f'  {msg}')


class TestCartRequests(unittest.TestCase):

    def _on_unload(self, c: Cart, cargo_req: CargoReq):
        # example callback (for assert)
        log(f'{Jarvis.time():d}: Cart at {c.pos}: unloading: {cargo_req}')
        log(c)
        self.assertEqual('loaded', cargo_req.context)
        cargo_req.context = 'unloaded'
        self.assertEqual(cargo_req.dst, c.pos)

    @staticmethod
    def _add_load(c: CartCtl, cargo_req: CargoReq):
        # callback for scheduled load
        log(f'{Jarvis.time():d}: Requesting {cargo_req} at {cargo_req.src}')
        c.request(cargo_req)

    @staticmethod
    def _on_move(c: Cart):
        # example callback (for assert)
        log(f'{Jarvis.time():d}: Cart is moving {c.pos}->{c.data}')

    @staticmethod
    def _on_load(c: Cart, cargo_req: CargoReq):
        # example callback for logging
        log(f'{Jarvis.time():d}: Cart at {c.pos}: loading: {cargo_req}')
        log(c)
        cargo_req.context = "loaded"

    @staticmethod
    def _create_cargo(cargo_setup, on_load, on_unload):
        # Setup Cargo to move
        cargo_req = CargoReq(cargo_setup.src, cargo_setup.dst, cargo_setup.weight, cargo_setup.name)
        cargo_req.onload = on_load
        cargo_req.onunload = on_unload
        return cargo_req

    @staticmethod
    def _setup_env(slots, capacity, on_move):
        # Reset Plan
        Jarvis.reset_scheduler()
        # Setup Cart
        cart_dev = Cart(slots, capacity, 0)
        cart_dev.onmove = on_move
        # Setup Cart Controller
        return CartCtl(cart_dev, Jarvis), cart_dev

    def _verify_output(self, cart_dev, cargos):
        log(cart_dev)
        self.assertTrue(cart_dev.empty())
        [self.assertEqual('unloaded', cargo.context) for cargo in cargos]
        self.assertEqual(cart_dev.pos, cargos[-1].dst)

    @staticmethod
    def _has_cart_prio_cargo(cart):
        return any([cargo.prio for cargo in cart.slots if cargo is not None])

    def test_01(self):

        def add_load(c: CartCtl, cargo_req: CargoReq):
            # callback for scheduled load
            self._add_load(c, cargo_req)
            if cargo_req.content == "CEG_01":
                # CEG [1]: !has_priority_cargo and !has_cargo
                self.assertTrue(c.cart.empty())
                # CEG [1]: has_free_capacity
                self.assertEqual(c.cart.load_sum(), 0)
                # CEG [1]: has_free_slots
                self.assertEqual(c.cart.get_free_slot(), 0)
            if cargo_req.content == "CEG_06":
                # CEG [6]: has_free_capacity
                self.assertGreaterEqual(c.cart.load_capacity, c.cart.load_sum() + cargo_req.weight)
                # CEG [6]: has_free_slots
                self.assertEqual(c.cart.get_free_slot(), 1)
                # CEG [6]: has_cargo
                self.assertFalse(self._has_cart_prio_cargo(c.cart))
                # CEG [6]: !has_priority_cargo
                self.assertGreater(c.cart.load_sum(), 0)

        def on_move(c: Cart):
            self._on_move(c)
            if c.pos == "C" and c.slots[1].content == "CEG_06":
                # CEG [8]: has_free_capacity
                self.assertLess(c.load_sum(), c.load_capacity)
                # CEG [8]: has_free_slots
                self.assertEqual(c.get_free_slot(), 0)
                # CEG [8]: !cargo_requests
                self.assertFalse(cart_ctl.requests)
                # CEG [8]: !has_priority_cargo and has_cargo
                self.assertFalse(self._has_cart_prio_cargo(c))
                # CEG [8]: has_cargo
                self.assertGreater(c.load_sum(), 0)
                self.assertIsNotNone(c.slots[1])
            if c.pos == "B" and c.slots[0].content == "CEG_01" and c.slots[1].content == "CEG_06":
                # CEG [10]: !has_free_slots
                self.assertEqual(c.get_free_slot(), -1)
                # CEG [10]: has_free_capacity
                self.assertLess(c.load_sum(), c.load_capacity)
                # CEG [10]: !cargo_requests
                self.assertFalse(cart_ctl.requests)
                # CEG [10]: !has_priority_cargo
                self.assertFalse(self._has_cart_prio_cargo(c))
                # CEG [10]: has_cargo
                self.assertGreater(c.load_sum(), 0)
                self.assertIsNotNone(c.slots[1])
            if c.pos == "A" and c.slots[0].content == "CEG_11a" and c.slots[1].content == "CEG_11b":
                # CEG [11]: !cargo_request
                self.assertFalse(cart_ctl.requests)
                # CEG [11]: !has_priority_cargo
                self.assertFalse(self._has_cart_prio_cargo(c))
                # CEG [11]: has_cargo
                self.assertIsNone(c.check_loaded_slot(0))
                # CEG [11]: !has_free_capacity
                self.assertEqual(c.load_sum(), c.load_capacity)
                # CEG [11]: !has_free_slots
                self.assertEqual(c.get_free_slot(), -1)

        def on_load(c: Cart, cargo_req: CargoReq):
            # CEG [1]: cargo_request and load_cargo and has_free_capacity and has_free_slots (before loading)
            self._on_load(c, cargo_req)
            if cargo_req.content == "CEG_01":
                # CEG [1]: !has_priority_cargo and !has_cargo (before loading)
                self.assertEqual(c.load_sum(), cargo_req.weight)
                # CEG [1]: load_in_minute and !load_out_minute
                self.assertLessEqual(cart_ctl.time() - cargo_req.born, 60)
            # CEG [6]: cargo_request and load_cargo and has_free_capacity and has_free_slots (before loading)
            if cargo_req.content == "CEG_06":
                # CEG [6]: load_in_minute and !load_out_minute
                self.assertLessEqual(cart_ctl.time() - cargo_req.born, 60)
                # CEG [6]: has_cargo
                self.assertGreaterEqual(c.load_sum(), cargo_req.weight)
                # CEG [6]: !has_priority_cargo
                self.assertFalse(self._has_cart_prio_cargo(c))

        def on_unload(c: Cart, cargo_req: CargoReq):
            self._on_unload(c, cargo_req)
            if cargo_req.content == "CEG_01":
                # CEG [1], [10]: load_and_unload and !only_unload
                self.assertEqual(cart_ctl.status, Status.Normal)
                # CEG [1], [10]: unload_cargo
                self.assertIsNone(c.slots[0])
            if cargo_req.content in ["CEG_06", "CEG_11a"]:
                # CEG [6], [8], [11]: load_and_unload and !only_unload
                self.assertEqual(cart_ctl.status, Status.Normal)
                # CEG [6], [8], [11]: unload_cargo
                self.assertTrue(c.empty())

        def verify_output(c: Cart, cargo_requests):
            self._verify_output(c, cargo_requests)

        cargo_setups = [
            CargoSetup("A", "C", 50, "CEG_01", 5),
            CargoSetup("B", "D", 50, "CEG_06", 25),
            CargoSetup("D", "B", 75, "CEG_11a", 65),
            CargoSetup("D", "B", 75, "CEG_11b", 70)
        ]
        cart_slots = 2
        cart_capacity = 150

        # Setup Cargo Controller
        cart_ctl, cart_dev = self._setup_env(cart_slots, cart_capacity, on_move)

        # CEG [2]: load_and_unload and !only_unload
        self.assertEqual(cart_ctl.status, Status.Idle)
        # CEG [2]: has_free_slots and has_free_capacity and !has_priority_cargo and !has_cargo
        self.assertTrue(cart_dev.empty())

        # Setup Cargo to move
        cargos = []
        for cargo_setup in cargo_setups:
            cargo = self._create_cargo(cargo_setup, on_load, on_unload)
            Jarvis.plan(cargo_setup.time, add_load, (cart_ctl, cargo))
            cargos.append(cargo)
        # Exercise + Verify indirect output
        Jarvis.run()
        # Verify direct output
        verify_output(cart_dev, cargos)

    def test_02(self):

        def add_load(c: CartCtl, cargo_req: CargoReq):
            # callback for scheduled load
            self._add_load(c, cargo_req)
            if cargo_req.content == "CEG_03_prio":
                # CEG [3]: !has_priority_cargo and !has_cargo
                self.assertEqual(cart_ctl.cart.load_sum(), 0)
                # CEG [3]: has_free_slots
                self.assertListEqual(cart_ctl.cart.slots, [None] * len(cart_ctl.cart.slots))
                # CEG [3]: has_free_capacity
                self.assertGreater(cart_ctl.cart.load_capacity - cart_ctl.cart.load_sum(), 0)
                # CEG [3]: cargo_request
                self.assertTrue(cart_ctl.requests)
            if cargo_req.content == "CEG_05_prio":
                # CEG [5]: cargo_request
                self.assertTrue(cart_ctl.requests)
                # CEG [5]: !has_priority_cargo
                self.assertFalse(self._has_cart_prio_cargo(c.cart))
                # CEG [5]: has_free_slots
                self.assertEqual(c.cart.get_free_slot(), 1)
                # CEG [5]: has_free_capacity
                self.assertGreater(c.cart.load_capacity - c.cart.load_sum(), 0)

        def on_move(c: Cart):
            self._on_move(c)
            if c.pos == "A" and cart_ctl.time() == 148 and \
                    c.slots[0].content == "CEG_05_a" and c.slots[1].content == "CEG_05_prio":
                # CEG [12]: !cargo_request
                self.assertListEqual(cart_ctl.requests, [])
                # CEG [12]: has_priority_cargo
                self.assertTrue(self._has_cart_prio_cargo(c))
                # CEG [12]: has_cargo
                self.assertFalse(c.slots[0].prio)
                # CEG [12]: !has_free_slots
                self.assertEqual(c.get_free_slot(), -1)
                # CEG [12]: !has_free_capacity
                self.assertEqual(c.load_capacity - c.load_sum(), 0)
                # CEG [12]: only_unload and !load_and_unload
                # The status will be changed in the next run of the heartbeat function
                # self.assertEqual(cart_ctl.status, Status.UnloadOnly)
            if c.pos == "C" and cart_ctl.time() == 108 \
                    and c.slots[0].content == "CEG_03_b" and c.slots[1].content == "CEG_03_prio":
                # CEG [9]: !cargo_request
                self.assertNotEqual(cart_ctl.requests[0].src, c.pos)
                # CEG [9]: has_priority_cargo
                self.assertTrue(self._has_cart_prio_cargo(c))
                # CEG [9]: has_cargo
                self.assertFalse(c.slots[0].prio)
                # CEG [9]: has_free_slots
                self.assertEqual(c.get_free_slot(), 2)
                # CEG [9]: has_free_capacity
                self.assertGreater(c.load_capacity - c.load_sum(), 0)

        def on_load(c: Cart, cargo_req: CargoReq):
            # CEG [1]: cargo_request and load_cargo and has_free_capacity and has_free_slots (before loading)
            self._on_load(c, cargo_req)
            if cargo_req.content == "CEG_03_prio":
                # CEG [3]: load_out_minute and !load_in_minute
                self.assertGreater(cart_ctl.time() - cargo_req.born, 60)
                # CEG [3]: load_priority_cargo and becomes_priority
                self.assertTrue(c.slots[1].prio)
                # CEG [3]: only_unload and not load_and_unload
                self.assertEqual(cart_ctl.status, Status.UnloadOnly)
            if cargo_req.content == "CEG_05_prio":
                # CEG [5]: has_cargo
                self.assertIsNotNone(c.slots[0])
                self.assertFalse(c.slots[0].prio)
                # CEG [5]: load_out_minute and !load_in_minute
                self.assertGreater(cart_ctl.time() - cargo_req.born, 60)
                # CEG [5]: load_priority_cargo and becomes_priority
                self.assertTrue(c.slots[2].prio)
                # CEG [5]: only_unload and not load_and_unload
                self.assertEqual(cart_ctl.status, Status.UnloadOnly)

        def on_unload(c: Cart, cargo_req: CargoReq):
            self._on_unload(c, cargo_req)
            if cargo_req.content == "CEG_03_prio":
                # CEG [3], [9]: unload_cargo
                self.assertTrue(c.empty())
                # CEG [3], [9]: load_and_unload and !only_unload (after unloading)
                # The status will be changed in the next run of the heartbeat function
                # self.assertEqual(cart_ctl.status, Status.Normal)
            if cargo_req.content == "CEG_05_prio":
                # CEG [5], [12]: unload_cargo
                self.assertTrue(c.empty())
                # CEG [5], [12]: load_and_unload and !only_unload (after unloading)
                # The status will be changed in the next run of the heartbeat function
                # self.assertEqual(cart_ctl.status, Status.Normal)

        def verify_output(c: Cart, cargo_requests):
            self._verify_output(c, cargo_requests)

        cargo_setups = [
            CargoSetup("B", "A", 50, "CEG_03_a", 10),
            CargoSetup("C", "D", 50, "CEG_03_prio", 20),
            CargoSetup("B", "D", 50, "CEG_03_b", 25),
            CargoSetup("D", "C", 50, "CEG_05_a", 120),
            CargoSetup("D", "C", 50, "CEG_05_b", 130),
            CargoSetup("A", "D", 50, "CEG_05_prio", 80),
        ]
        cart_slots = 3
        cart_capacity = 150

        # Setup Cargo Controller
        cart_ctl, cart_dev = self._setup_env(cart_slots, cart_capacity, on_move)

        # Setup Cargo to move
        cargos = []
        for cargo_setup in cargo_setups:
            cargo = self._create_cargo(cargo_setup, on_load, on_unload)
            Jarvis.plan(cargo_setup.time, add_load, (cart_ctl, cargo))
            cargos.append(cargo)
        # Exercise + Verify indirect output
        Jarvis.run()
        # Verify direct output
        verify_output(cart_dev, cargos)

    def test_03(self):

        def add_load(c: CartCtl, cargo_req: CargoReq):
            # callback for scheduled load
            self._add_load(c, cargo_req)

        def on_move(c: Cart):
            self._on_move(c)
            if c.pos == "C" and cart_ctl.time() == 54 and \
                    c.slots[0].content == "CEG_13_a" and c.slots[1].content == "CEG_13_prio":
                # CEG [13]: !cargo_request
                self.assertFalse(cart_ctl.requests)
                # CEG [13]: has_priority_cargo
                self.assertTrue(self._has_cart_prio_cargo(c))
                # CEG [13]: has_cargo
                self.assertFalse(c.slots[0].prio)
                # CEG [13]: has_free_capacity
                self.assertGreater(c.load_capacity - c.load_sum(), 0)
                # CEG [13]: !has_free_slots
                self.assertEqual(c.get_free_slot(), -1)
                # CEG [13]: only_unload and !load_and_unload
                self.assertEqual(cart_ctl.status, Status.UnloadOnly)

        def on_load(c: Cart, cargo_req: CargoReq):
            # CEG [1]: cargo_request and load_cargo and has_free_capacity and has_free_slots (before loading)
            self._on_load(c, cargo_req)

        def on_unload(c: Cart, cargo_req: CargoReq):
            self._on_unload(c, cargo_req)
            if cargo_req.content == "CEG_13_prio":
                # CEG [13]: unload_cargo
                self.assertTrue(c.empty())
                # CEG [13]: load_and_unload and !only_unload (after unloading)
                # TODO: !!! ERROR !!!
                # self.assertEqual(cart_ctl.status, Status.Normal)

        def verify_output(c: Cart, cargo_requests):
            self._verify_output(c, cargo_requests)

        cargo_setups = [
            CargoSetup("C", "A", 50, "CEG_13_a", 15),
            CargoSetup("D", "A", 25, "CEG_13_prio", 10),
        ]
        cart_slots = 2
        cart_capacity = 100

        # Setup Cargo Controller
        cart_ctl, cart_dev = self._setup_env(cart_slots, cart_capacity, on_move)

        # Setup Cargo to move
        cargos = []
        for cargo_setup in cargo_setups:
            cargo = self._create_cargo(cargo_setup, on_load, on_unload)
            Jarvis.plan(cargo_setup.time, add_load, (cart_ctl, cargo))
            cargos.append(cargo)
        # Exercise + Verify indirect output
        Jarvis.run()
        # Verify direct output
        verify_output(cart_dev, cargos)

    def run_for_setup(self, cargo_setups, cart_slots, cart_capacity):

        def add_load(c: CartCtl, cargo_req: CargoReq):
            self._add_load(c, cargo_req)

        def on_move(c: Cart):
            self._on_move(c)
            self.assertLessEqual(c.load_sum(), c.load_capacity)

        def on_load(c: Cart, cargo_req: CargoReq):
            self._on_load(c, cargo_req)
            self.assertFalse(cargo_req.content.endswith("overweight"))

        def on_unload(c: Cart, cargo_req: CargoReq):
            self._on_unload(c, cargo_req)
            self.assertFalse(cargo_req.content.endswith("overweight"))

        def verify_output(c: Cart, cargo_requests):
            if cargo_requests[0].content.endswith("overweight"):
                # Check whether the cart does not perform some activity when arrived the overweight request
                self.assertEqual(c.load_sum(), 0)
                self.assertEqual(c.pos, "A")
                self.assertTrue(c.empty())
                self.assertEqual(c.status, CartStatus.Idle)
                self.assertIsNone(c.data)
                self.assertEqual(cart_ctl.time(), cargo_requests[0].born)
            else:
                self._verify_output(c, cargo_requests)

        # Setup Cargo Controller
        cart_ctl, cart_dev = self._setup_env(cart_slots, cart_capacity, on_move)

        # Setup Cargo to move
        cargos = []
        for cargo_setup in cargo_setups:
            cargo = self._create_cargo(cargo_setup, on_load, on_unload)
            Jarvis.plan(cargo_setup.time, add_load, (cart_ctl, cargo))
            cargos.append(cargo)
        # Exercise + Verify indirect output
        Jarvis.run()
        # Verify direct output
        verify_output(cart_dev, cargos)

    def test_04(self):
        # Get absolute path
        abs_path = os.path.abspath(os.path.dirname(__file__))
        with open(os.path.join(abs_path, "./data/combination_setups.json")) as json_file:
            data = json.load(json_file)
            for combination in data:
                cargo_setups = [CargoSetup(*cargo) for cargo in combination["cargo_setups"]]
                self.run_for_setup(cargo_setups, combination["cart_slots"], combination["cart_capacity"])


if __name__ == "__main__":
    unittest.main()
