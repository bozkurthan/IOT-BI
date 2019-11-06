# Scenario-1 --> Edge-Clients have model

## EDGE CLIENTS CONFIGS:

### CLIENT-1:

```python
client_ID = "CC0"

_client_will_sub = False

_client_has_model = True

test_packet_length = 100

sub_broker_address = "0.0.0.0" #DOESN'T MATTER
sub_broker_port = 1883 #DOESN'T MATTER
client_sub_topic = "test" #DOESN'T MATTER

pub_broker_address = "1.1.1.1"  #FOG-1 MATTER
pub_broker_port = 1883
client_pub_topic = "test"
publish_delay_time = 0.2
publish_size = 10
client_number = "C1"
location_number = "L1"
packet_name=location_number+ "-"+ client_number
```

}
FOG CLIENTS CONFIGS (AFTER EDGE CLIENTS):
{

}
CLOUD CLIENTS CONFIGS:
{

}
FOG-2 CLIENT CONFIGS:
{

}
SERVER CLIENT CONFIG
{

}
