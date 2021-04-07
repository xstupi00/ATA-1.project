# Text Definition

## Cause-Effect Graph

![text](Project_name.svg)

### Causes:

```
cargo_request: Vznik požiadavky na presun materiálu z jedného miesta do druhého
load_in_minute: Vozík si materiál vyzdvihne do 1 minúty od vzniku požiadavky
load_out_minute: Vozík si materiál vyzdvihne po 1 minúte od vzniku požiadavky
has_priority_cargo: Vozík má naložený prioritný materiál
has_free_slots: Vozík ma voľný dostatočný počet slotov vozíka
has_free_capacity: Vozík má voľnú dostatočnú kapacitu
has_cargo: Vozík má naložený materiál
```

### Effects:

```
load_cargo: Vozík vyzdvihne materiál
load_priority_cargo: Vozík vyzdvihne prioritný materiál
becomes_priority: Materiál sa stáva prioritným
expired_time: Vozík nestihol vyzdvihnúť náklad v požadovanom limite
only_unload: Vozík je v režíme iba_vykládka
load_and_unload: Vozík je v režíme nákladka_výkladka
unload_cargo: Vozík vykladá už vyzdvihnuté materiály
```

### Rules:

```
has_no_priority_cargo = !has_priority_cargo
no_load_in_minute = !load_in_minute
no_load_out_minute = !load_out_minute
load_cargo = has_no_priority_cargo && load_in_minute
load_priority_cargo = has_no_priority_cargo && load_out_minute
becomes_priority = no_load_in_minute && cargo_request
expired_time = cargo_request && no_load_in_minute && no_load_out_minute
only_unload = load_out_minute || has_priority_cargo
load_and_unload = no_load_out_minute && has_no_priority_cargo
unload_cargo = load_in_minute || load_out_minute || has_cargo
```

### Constraints:

```
E: load_in_minute, load_out_minute, has_priority_cargo
I: has_free_capacity, has_cargo
I: has_free_slots, has_cargo
load_in_minute->cargo_request
load_out_minute->cargo_request
load_in_minute->has_free_slots
load_in_minute->has_free_capacity
load_out_minute->has_free_slots
load_out_minute->has_free_capacity
has_priority_cargo->has_cargo
only_unload masks load_and_unload
load_and_unload masks only_unload
```


# Test Cases

### [1]

```
cargo_request: 1
load_in_minute: 1
load_out_minute: 0
has_priority_cargo: 0
has_free_slots: 1
has_free_capacity: 1
has_cargo: 0
load_cargo: true
load_priority_cargo: false
becomes_priority: false
expired_time: false
only_unload: false
load_and_unload: true
unload_cargo: true
```
### [2]

```
cargo_request: 0
load_in_minute: 0
load_out_minute: 0
has_priority_cargo: 0
has_free_slots: 1
has_free_capacity: 1
has_cargo: 0
load_cargo: false
load_priority_cargo: false
becomes_priority: false
expired_time: false
only_unload: false
load_and_unload: true
unload_cargo: false
```
### [3]

```
cargo_request: 1
load_in_minute: 0
load_out_minute: 1
has_priority_cargo: 0
has_free_slots: 1
has_free_capacity: 1
has_cargo: 0
load_cargo: false
load_priority_cargo: true
becomes_priority: true
expired_time: false
only_unload: true
load_and_unload: false
unload_cargo: true
```
### [4]

```
cargo_request: 1
load_in_minute: 0
load_out_minute: 0
has_priority_cargo: 0
has_free_slots: 1
has_free_capacity: 1
has_cargo: 0
load_cargo: false
load_priority_cargo: false
becomes_priority: true
expired_time: true
only_unload: false
load_and_unload: true
unload_cargo: false
```
### [5]

```
cargo_request: 1
load_in_minute: 0
load_out_minute: 1
has_priority_cargo: 0
has_free_slots: 1
has_free_capacity: 1
has_cargo: 1
load_cargo: false
load_priority_cargo: true
becomes_priority: true
expired_time: false
only_unload: true
load_and_unload: false
unload_cargo: true
```
### [6]

```
cargo_request: 1
load_in_minute: 1
load_out_minute: 0
has_priority_cargo: 0
has_free_slots: 1
has_free_capacity: 1
has_cargo: 1
load_cargo: true
load_priority_cargo: false
becomes_priority: false
expired_time: false
only_unload: false
load_and_unload: true
unload_cargo: true
```
### [7]

```
cargo_request: 1
load_in_minute: 0
load_out_minute: 0
has_priority_cargo: 0
has_free_slots: 1
has_free_capacity: 1
has_cargo: 1
load_cargo: false
load_priority_cargo: false
becomes_priority: true
expired_time: true
only_unload: false
load_and_unload: true
unload_cargo: true
```
### [8]

```
cargo_request: 0
load_in_minute: 0
load_out_minute: 0
has_priority_cargo: 0
has_free_slots: 1
has_free_capacity: 1
has_cargo: 1
load_cargo: false
load_priority_cargo: false
becomes_priority: false
expired_time: false
only_unload: false
load_and_unload: true
unload_cargo: true
```
### [9]

```
cargo_request: 0
load_in_minute: 0
load_out_minute: 0
has_priority_cargo: 1
has_free_slots: 1
has_free_capacity: 1
has_cargo: 1
load_cargo: false
load_priority_cargo: false
becomes_priority: false
expired_time: false
only_unload: true
load_and_unload: false
unload_cargo: true
```
### [10]

```
cargo_request: 0
load_in_minute: 0
load_out_minute: 0
has_priority_cargo: 0
has_free_slots: 0
has_free_capacity: 1
has_cargo: 1
load_cargo: false
load_priority_cargo: false
becomes_priority: false
expired_time: false
only_unload: false
load_and_unload: true
unload_cargo: true
```
### [11]

```
cargo_request: 0
load_in_minute: 0
load_out_minute: 0
has_priority_cargo: 0
has_free_slots: 0
has_free_capacity: 0
has_cargo: 1
load_cargo: false
load_priority_cargo: false
becomes_priority: false
expired_time: false
only_unload: false
load_and_unload: true
unload_cargo: true
```
### [12]

```
cargo_request: 0
load_in_minute: 0
load_out_minute: 0
has_priority_cargo: 1
has_free_slots: 0
has_free_capacity: 0
has_cargo: 1
load_cargo: false
load_priority_cargo: false
becomes_priority: false
expired_time: false
only_unload: true
load_and_unload: false
unload_cargo: true
```
### [13]

```
cargo_request: 0
load_in_minute: 0
load_out_minute: 0
has_priority_cargo: 1
has_free_slots: 0
has_free_capacity: 1
has_cargo: 1
load_cargo: false
load_priority_cargo: false
becomes_priority: false
expired_time: false
only_unload: true
load_and_unload: false
unload_cargo: true
```
