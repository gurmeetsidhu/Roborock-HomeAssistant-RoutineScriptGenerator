# Roborock Routine-Like Control from Home Assistant or Google Home

## The Usecase

My usecase for this was primarily fueled by:
- No easy way to vacuum then mop a zone, or a room without setting up custom routines
- Home assistant integration currently doesn't have support for routines :(
- My primarily Google Home based ecosystem doesn't support running routines with Roborock's integration

## The Solution

My solution ain't pretty, so I was looking for how I can potentially improve the reliability, jank, and/or extensive copy pasta I need to do. Here's what it does: 

1. I have a input_select variable setup in Home Assistant of all the areas that my partner and I regularly clean with/without the Roborock (living room, entry carpet, other zones/rooms)
2. I have an automation that triggers when input_select variable changes:
    1. It changes the mop/vacuum mode to allow for vacuum first 
    2. Triggers clean segment/zone 
    3. Wait for trigger from Roborock when it is back in a fresh state (i.e. done docking, emptying, etc)
    4. Then set the mop/vacuum mode to allow for moping next
    5. Repeat cleaning segment/zone
    6. Wait again for Roborock to dock, empty, wash, etc. 
3. The automation's behaviour is set up to queue. So it will handle multiple requests one at a time instead of stopping its current job. Great! BUT .... I can't change the order of the queue so it does all vacuuming in one go then the mopping, it does areas at a time.
4. Creating the automation above is difficult so I created a script to generate the YAML. There is a configuration variable that allows you to input locations, preferred fan_speeds, mopping intensity, and more. 
5. Finally I setup an extensive catch all Google Assistant automations in Google Home Script editor to handle the different ways I'll inevitably say the command wrong (highly unreliable otherwise, kitchen work area != kitchen working area and Google shits itself). Same script generates the YAML here too. 
The end result is nice, I like being able to ask it to clean different segments now while my partner cook, clean and eat without having to worry about it smashing into our feet, miss an area. 
What I would like to improve is the reliability. I wish there was a way that Google had setup their                                                              SDK to be more conversational like DialogueFlow so I can pass back some troubleshooting, or ask for prompts (such as: do you just want to vacuum, mop or do both this time? etc.)
