# OSI DUMP RELEASE NOTES

## 0.1.3.2.2

- Added a work around for homemade Openstack client trying both HTTP and HTTPS

## 0.1.3.2.3

- Added created time, updated_time for load balancer

## 0.1.3.2.8

- Added vlan id for external ports
- Added flavor id and image id for instances

## 0.1.3.2.9

- Added network name for external ports

## 0.1.3.3

- Hot fix extennal port model vlan id string -> int

## 0.1.3.3.1

- Optimize role assignment fetch

## 0.1.3.3.2

- Hot fix role assignment fetch, added `v3` into endpoint

## 0.1.3.3.2.4

- Revert role assignment optimization for backward compatibility

## 0.1.3.3.2.5

- Revert openstacksdk version back to 3.3.0

## 0.1.3.3.2.6

- Optimize role assignment with caching

## 0.1.3.3.2.8

- Fix image properties

## 0.1.3.3.2.9

- Added log for failure reason when fetching instances

## 0.1.3.3.3.0

- Added `validate=False` to connection

## 0.1.3.3.3.1

- Removed `validate=False`

## 0.1.3.3.3.2

- Added `interface` to auth information (default to `'public'`)

## 0.1.3.3.3.3

- Add vip for lb, role for amphorae

## 0.1.3.3.3.5

- Add lb count for project sheet

## 0.1.3.3.3.6

- Add amphorae flavor, description for lb sheet