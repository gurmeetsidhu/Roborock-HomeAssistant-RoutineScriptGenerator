def generate_home_assistant_yaml(areas):
    
  for area in list(roborock_mapping.keys()):
    mapping = roborock_mapping[area]
    yaml = f"""      - conditions:
          - condition: state
            entity_id: input_select.roomba_to_clean_area_mode
            state: {area}
        sequence:
          - alias: Set Roborock's Fan Speed to {mapping["fan"]}
            service: vacuum.set_fan_speed
            target:
              entity_id: vacuum.roborock_q_revo
            data:
              fan_speed: {mapping["fan"]}
          - service: vacuum.send_command
            target:
              entity_id: vacuum.roborock_q_revo
            data:
              command: set_water_box_custom_mode
              params: 200
            alias: Turn off Roborock's Mop"""
    if "coordinates" in mapping:
        yaml += f"""
          - service: roborock.vacuum_clean_zone
            target:
              entity_id:
                - vacuum.roborock_q_revo
              device_id: []
              area_id: []
            data:
              zone:"""
        for coordinate in mapping["coordinates"]:
            yaml += f"""
                - - {coordinate[0]}
                  - {coordinate[1]}
                  - {coordinate[2]}
                  - {coordinate[3]}"""
    elif "segment" in mapping:
        yaml += f"""
          - service: roborock.vacuum_clean_segment
            target:
              entity_id:
                - vacuum.roborock_q_revo
              device_id: []
              area_id: []
            data:
              segments: {mapping["segment"]}"""
    yaml += f"""
              repeats: {mapping["repeats"]}
          - delay:
              hours: 0
              minutes: 2
              seconds: 0
              milliseconds: 0
          - wait_for_trigger:
              - platform: state
                entity_id:
                  - vacuum.roborock_q_revo
                attribute: inFreshState
                from: 0
                to: 1
                alias: When Roborock theoretically finishes routine
            timeout:
              hours: 1
              minutes: 0
              seconds: 0
              milliseconds: 0
            continue_on_timeout: false"""
    if mapping["mop"] != 200:
        yaml += f"""
          - alias: Set Roborock's Fan Speed to Off
            service: vacuum.set_fan_speed
            target:
              entity_id: vacuum.roborock_q_revo
            data:
              fan_speed: "off"
          - alias: Turn On Roborock's Mop to current custom setting
            service: vacuum.send_command
            target:
              entity_id: vacuum.roborock_q_revo
            data:
              command: set_water_box_custom_mode
              params: {mapping["mop"]}"""
        if "coordinates" in mapping:
            yaml += f"""
          - service: roborock.vacuum_clean_zone
            target:
              entity_id:
                - vacuum.roborock_q_revo
              device_id: []
              area_id: []
            data:
              zone:"""
            for coordinate in mapping["coordinates"]:
                yaml += f"""
                - - {coordinate[0]}
                  - {coordinate[1]}
                  - {coordinate[2]}
                  - {coordinate[3]}"""
        elif "segment" in mapping:
            yaml += f"""
          - service: roborock.vacuum_clean_segment
            target:
              entity_id:
                - vacuum.roborock_q_revo
              device_id: []
              area_id: []
            data:
              segments: {mapping["segment"]}"""
        yaml += f"""
              repeats: {mapping["repeats"]}
            enabled: true
          - delay:
              hours: 0
              minutes: 2
              seconds: 0
              milliseconds: 0
          - wait_for_trigger:
              - platform: state
                entity_id:
                  - vacuum.roborock_q_revo
                attribute: inFreshState
                from: 0
                to: 1
                alias: When Roborock theoretically finishes routine
            timeout:
              hours: 1
              minutes: 0
              seconds: 0
              milliseconds: 0
            continue_on_timeout: false"""
    print(yaml)

def generate_google_home_script(areas):
    for area in list(roborock_mapping.keys()):
        mapping = roborock_mapping[area]
        yaml = f"""

metadata:
  name: Clean the {area}
  description: Script to {mapping["assistant_response"][19:]}.

automations:
  starters:"""
        for item in [area] + mapping["alternatives"]:
            yaml += f"""
    - type: assistant.event.OkGoogle
      eventData: query
      is: tell Roborock to clean {item}
    - type: assistant.event.OkGoogle
      eventData: query
      is: clean {item}
    - type: assistant.event.OkGoogle
      eventData: query
      is: change the area mode to {item}"""

        yaml += f"""

  actions:
    - type: assistant.command.OkGoogle
      okGoogle: Change the area mode to {area}
      devices: Kitchen Speaker - Kitchen
    - type: assistant.command.Broadcast
      message: {mapping["assistant_response"]}
      devices: Kitchen Speaker - Kitchen
"""
        print(yaml)
        
        

roborock_mapping = {

"the entry mats": {"fan": "max_plus", "mop": 200, "vacuum": True, "coordinates": [[26050,21900,26950,23800],[18650,21950,20000,22600]], "repeats": 2, 
                    "alternatives": ["the door mats", "the shoe mats", "the outdoor mats", "entrance mats", "the entrance mats", "both entrance mats", "the two entrance mats"], 
                    "assistant_response": "Got it, Roborock will vacuum just the two entrance mats"},
"around the stove": {"fan": "max", "mop": 207, "vacuum": True, "coordinates": [[20950, 24750, 22950, 25850]], "repeats": 2, 
                    "alternatives": ["near the stove", "under the stove", "the stove area"], 
                    "assistant_response": "Got it, Roborock will vacuum then mop the area in front of the stove"},
"around the fridge": {"fan": "max", "mop": 207, "vacuum": True, "coordinates": [[21100,22050,22850,23100]], "repeats": 2, 
                    "alternatives": ["near the fridge", "under the fridge", "the fridge area"], 
                    "assistant_response": "Got it, Roborock will vacuum then mop the area in front of the fridge"},
"kitchen work area": {"fan": "max", "mop": 207, "vacuum": True, "coordinates": [[21900,24800,24200,25850],[21900,22050,22550,24850]], "repeats": 2, 
                    "alternatives": ["the kitchen work area", "around the sink"], 
                    "assistant_response": "Got it, Roborock will vacuum then mop the areas around the counters, stove, and fridge"},
"around the table": {"fan": "balanced", "mop": 207, "vacuum": True, "coordinates": [[21950, 22700, 24000, 24650]], "repeats": 2, 
                    "alternatives": ["near the kitchen table", "the kitchen table", "under the kitchen table", "under the table"], 
                    "assistant_response": "Got it, Roborock will vacuum and then mop the area under and around the kitchen table"},
"the living room carpet": {"fan": "balanced", "mop": 200, "vacuum": True, "coordinates": [[23650,21850,26100,23550]], "repeats": 2, 
                    "alternatives": ["the living room rug", "the rug"], 
                    "assistant_response": "Got it, Roborock will vacuum the area rug in the living room"},
"living room": {"fan": "max", "mop": 207, "vacuum": True, "segment": 20, "repeats": 1, 
                    "alternatives": ["the den", "the living room", "TV Area"], 
                    "assistant_response": "Got it, Roborock will vacuum then mop the entire living room"},
"kitchen": {"fan": "balanced", "mop": 207, "vacuum": True, "segment": 18, "repeats": 1, 
                    "alternatives": ["the kitchen", "the dining room"], 
                    "assistant_response": "Got it, Roborock will vacuum then mop the entire kitchen"},
"hallway": {"fan": "quiet", "mop": 207, "vacuum": True, "segment": 21, "repeats": 1, 
                    "alternatives": ["our hallway", "the hallway", "the interior hallway", "interior hallway"], 
                    "assistant_response": "Got it, Roborock will vacuum then mop the entire interior hallway"},
"entry hallway": {"fan": "max", "mop": 207, "vacuum": True, "segment": 16, "repeats": 1, 
                    "alternatives": ["the front hallway", "front hallway", "the entry hallway", "entrance hallway", "front entrance hallway", "the entrance", "entrance"], 
                    "assistant_response": "Got it, Roborock will vacuum then mop the entire front entrance hallway"},
"guest bathroom": {"fan": "turbo", "mop": 203, "vacuum": True, "segment": 17, "repeats": 1, 
                    "alternatives": ["other bathroom", "the guest bathroom", "the other bathroom"], 
                    "assistant_response": "Got it, Roborock will vacuum then mop the entire guest bathroom"},
"our bedroom": {"fan": "quiet", "mop": 207, "vacuum": True, "segment": 19, "repeats": 1, 
                    "alternatives": ["the bedroom", "bedroom", "around the bed", "bed area", "the bed area"], 
                    "assistant_response": "Got it, Roborock will vacuuum then mop your entire bedroom"},
"our bathroom": {"fan": "balanced", "mop": 203, "vacuum": True, "segment": 22, "repeats": 1, 
                    "alternatives": ["main bathroom", "the main bathroom", "master bathroom", "the master bathroom"], 
                    "assistant_response": "Got it, Roborock will vacuuum then mop your entire bathroom"},
"office": {"fan": "quiet", "mop": 207, "vacuum": True, "segment": 23, "repeats": 1, 
                    "alternatives": ["the office", "guest bedroom", "the guest bedroom"], 
                    "assistant_response": "Got it, Roborock will vacuuum then mop the entire office"},

}

# generate_home_assistant_yaml(roborock_mapping)
generate_google_home_script(roborock_mapping)