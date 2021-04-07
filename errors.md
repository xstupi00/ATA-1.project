## 1. An incorrect switching to ``UnloadOnly`` status. ##

- **Specification**: The cart switches to status ``UnloadOnly`` when loads some request with priority.
- **Implementation**: The cart switches to status ``UnloadOnly`` when exists some request with priority.
- **Replication**:

```       
cargo_setups = [
    CargoSetup("B", "A", 50, "REQUEST_A", 10),
    CargoSetup("C", "D", 50, "REQUEST_B", 20),
]
Cart(2, 100, 0)
```

- **Real output**:

```
10: Requesting CargoReq(REQUEST_A) at B
10: Cart is moving A->B
20: Requesting CargoReq(REQUEST_B) at C
32: Cart at B: loading: CargoReq(REQUEST_A)
Cart(pos=B, Status.Idle, data=None, maxload=100, slots=['CargoReq(REQUEST_A)', 'None'])
32: Cart is moving B->A
64: Cart at A: unloading: CargoReq(REQUEST_A)
Cart(pos=A, Status.Idle, data=None, maxload=100, slots=['None', 'None'])
64: Cart is moving A->B
84: Cart is moving B->C
Do not know what to do at time 104
Cart(pos=C, Status.Idle, data=None, maxload=100, slots=['None', 'None']
```

- **Expected output**:

```
10: Requesting CargoReq(REQUEST_A) at B
10: Cart is moving A->B
20: Requesting CargoReq(REQUEST_B) at C
32: Cart at B: loading: CargoReq(REQUEST_A)
Cart(pos=B, Status.Idle, data=None, maxload=100, slots=['CargoReq(REQUEST_A)', 'None'])
32: Cart is moving B->A
64: Cart at A: unloading: CargoReq(REQUEST_A)
Cart(pos=A, Status.Idle, data=None, maxload=100, slots=['None', 'None'])
64: Cart is moving A->B
84: Cart is moving B->C
106: Cart at C: loading: PriorityCargoReq(REQUEST_B)
Cart(pos=C, Status.Idle, data=None, maxload=100, slots=['PriorityCargoReq(REQUEST_B)', 'None'])
106: Cart is moving C->D
128: Cart at D: unloading: PriorityCargoReq(REQUEST_B)
Cart(pos=D, Status.Idle, data=None, maxload=100, slots=['None', 'None'])
Do not know what to do at time 128
Cart(pos=D, Status.Idle, data=None, maxload=100, slots=['None', 'None'])
```

- **Source of the error**: ``REQUEST_B`` is created when ``20 seconds``, thus in  ``80 seconds`` it becomes a priority.  The cart is moving from ``B`` to ``C`` when ``84 seconds`` and at this moment the controller sets the status ``UnloadOnly``, because there are the priority request.  When the cart reaches the source station of the ``REQUEST_B`` (``C``), due to this status will not be allowed to load this request.  It is caused by the conditioned statement ``self.status != Status.UnloadOnly`` in the [file](../cartctl.py) at ``line 158``.
  
- **Suggestion of error correction**: Removal of the mentioned condition, because the status is checked in other places.  Mainly, the function ``try_load_here_single`` called from this conditioned branch, performs the status check whether the loading of new cargo is allowed.

## 2. An incorrect switching to ``Normal`` status. ##

- **Specification**: The cart switches to status ``Normal`` when unloading all loaded priority cargo.
- **Implementation**: The cart switches to status ``Normal`` when does not exist request with priority.
- **Replication**:

```       
cargo_setups = [
    CargoSetup("B", "A", 50, "REQUEST_A", 10),
    CargoSetup("C", "A", 50, "REQUEST_B", 20),
    CargoSetup("D", "B", 50, "REQUEST_C", 100)
]
Cart(2, 100, 0)
```

- **Real output**:

```
10: Requesting CargoReq(REQUEST_A) at B
10: Cart is moving A->B
20: Requesting CargoReq(REQUEST_B) at C
32: Cart at B: loading: CargoReq(REQUEST_A)
Cart(pos=B, Status.Idle, data=None, maxload=100, slots=['CargoReq(REQUEST_A)', 'None'])
32: Cart is moving B->A
64: Cart at A: unloading: CargoReq(REQUEST_A)
Cart(pos=A, Status.Idle, data=None, maxload=100, slots=['None', 'None'])
64: Cart is moving A->B
84: Cart is moving B->C
100: Requesting CargoReq(REQUEST_C) at D
106: Cart at C: loading: PriorityCargoReq(REQUEST_B)
Cart(pos=C, Status.Idle, data=None, maxload=100, slots=['PriorityCargoReq(REQUEST_B)', 'None'])
106: Cart is moving C->D
128: Cart at D: loading: CargoReq(REQUEST_C)
Cart(pos=D, Status.Idle, data=None, maxload=100, slots=['PriorityCargoReq(REQUEST_B)', 'CargoReq(REQUEST_C)'])
128: Cart is moving D->A
140: Cart at A: unloading: PriorityCargoReq(REQUEST_B)
Cart(pos=A, Status.Idle, data=None, maxload=100, slots=['None', 'CargoReq(REQUEST_C)'])
140: Cart is moving A->B
162: Cart at B: unloading: CargoReq(REQUEST_C)
Cart(pos=B, Status.Idle, data=None, maxload=100, slots=['None', 'None'])
Do not know what to do at time 162
Cart(pos=B, Status.Idle, data=None, maxload=100, slots=['None', 'None'])
```

- **Expected output**:

```
10: Requesting CargoReq(REQUEST_A) at B
10: Cart is moving A->B
20: Requesting CargoReq(REQUEST_B) at C
32: Cart at B: loading: CargoReq(REQUEST_A)
Cart(pos=B, Status.Idle, data=None, maxload=100, slots=['CargoReq(REQUEST_A)', 'None'])
32: Cart is moving B->A
64: Cart at A: unloading: CargoReq(REQUEST_A)
Cart(pos=A, Status.Idle, data=None, maxload=100, slots=['None', 'None'])
64: Cart is moving A->B
84: Cart is moving B->C
100: Requesting CargoReq(REQUEST_C) at D
106: Cart at C: loading: PriorityCargoReq(REQUEST_B)
Cart(pos=C, Status.Idle, data=None, maxload=100, slots=['PriorityCargoReq(REQUEST_B)', 'None'])
106: Cart is moving C->D
126: Cart is moving D->A
138: Cart at A: unloading: PriorityCargoReq(REQUEST_B)
Cart(pos=A, Status.Idle, data=None, maxload=100, slots=['None', 'None'])
138: Cart is moving A->B
158: Cart is moving B->C
178: Cart is moving C->D
200: Cart at D: loading: PriorityCargoReq(REQUEST_C)
Cart(pos=D, Status.Idle, data=None, maxload=100, slots=['PriorityCargoReq(REQUEST_C)', 'None'])
200: Cart is moving D->A
210: Cart is moving A->B
232: Cart at B: unloading: PriorityCargoReq(REQUEST_C)
Cart(pos=B, Status.Idle, data=None, maxload=100, slots=['None', 'None'])
Do not know what to do at time 232
Cart(pos=B, Status.Idle, data=None, maxload=100, slots=['None', 'None'])
```

- **Source of the error**: The cart loads the ``REQUEST_C`` when time ``104 seconds``, and since this request was created in time ``20 seconds``, so it has been load with priority. When loading this request, the cart is in the ``UnloadOnly`` status. However, subsequently, the cart is moving from ``C`` to ``D`` in time ``106 seconds`` and since does not exist the priority request, the cart will switch to the ``Normal`` status. This switching is caused by the code section in the [file](../cartctl.py) at ``lines 146-153``. As a result, the cart at station ``D`` loads the cargo even though it has priority cargo on board.
  
- **Suggestion of error correction**: The cart should not switch to status ``UnloadOnly`` according to the existence of a priority request, but according to the presence of priority cargo on board. The addition of the following conditioned statement ``any(s.prio for s in self.cart.slots if s is not None)`` to `line 150` in the [file](../cartctl.py) can suppress this problem.
