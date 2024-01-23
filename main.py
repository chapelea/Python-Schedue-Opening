# Written by: Ethan Chapel
# Date: 1/17/2024

# Class to represent an event with data such as whos schedule it belongs to as well as the time it starts and ends.
class Event:
  def __init__(self, person, start_time, end_time, label):
    self.person = person
    self.start_time = start_time
    self.end_time = end_time
    self.label = label

  # Function to change the person
  def change_person(self, new_person):
    self.person = new_person
    
  # Function to change the start time
  def change_start_time(self, new_start_time):
    self.start_time = new_start_time
    
  # Function to change the end time
  def change_end_time(self, new_end_time):
    self.end_time = new_end_time
    
  # Function to change the label
  def change_label(self, new_label):
    self.label = new_label 
    
  # Overriding the __str__ function to print the event
  def __str__(self):
    return self.person + ": " + self.label + " (" + time_to_float(self.start_time) + " - " + time_to_float(self.end_time) + ")"


# Function to convert a time string to a float and vice versa
def time_to_float(time):
  if type(time) == str:
    formated_time = time.split(" ")[0]
    if time.split(" ")[1].lower() == "pm":
      formated_time = str(int(formated_time.split(":")[0]) + 12) + ":" + formated_time.split(":")[1]
    
    return float(formated_time.split(":")[0]) + float(formated_time.split(":")[1])/60

  elif type(time) == float:
    am_pm = " am"
    if time > 12:
      time -= 12
      am_pm = " pm"

    # Formating midnight hour to "12:mm am"
    if time - (time % 1) == 0:
      time += 12

    # Enforces the format of the time
    if int(round((time % 1) * 60)) < 10:
      new_time = str(int(time - (time % 1))) + ":0" + str(int(round((time % 1) * 60))) + am_pm
    else:
        new_time = str(int(time - (time % 1))) + ":" + str(int(round((time % 1) * 60))) + am_pm
      
    return new_time


def delete_openings(week):
  new_week = {"Sun": [],
    "Mon": [],
    "Tue": [],
    "Wed": [],
    "Thu": [],
    "Fri": [],
    "Sat": []}
  for day in week:
    for event in week[day]:
      if event.person != "Opening":
        new_week[day].append(event)
  return new_week

  

# Prints a menu of options for the user to choose from
def print_menu():
  print("Please select one of the following number options:")
  print("1. Add new event(s)")
  print("2. Show week")
  print("3. Find openings")
  print("4. Delete all events")
  print("-1. Exit")
  return True


# Function to add new events to the schedule
def add_event(week):
  try:
    print("How many unique events do you want to add?")
    num_events = int(input())

    for _ in range(num_events):
      print("Please enter the following information:")
      print("(type 'exit' into the person field to exit)")
      person = input("Person: ")
      if person == "exit":
        break

      print("(times should be in the format of 'hh:mm am' or 'hh:mm pm')")
      start_time = input("Start time: ")
      end_time = input("End time: ")
      label = input("Label: ")

      start_time = time_to_float(start_time)
      end_time = time_to_float(end_time)
    
      event = Event(person, start_time, end_time, label) # Create a new event
    
      print("What day(s) does this event take place?")
      print("Please enter days as the first 3 letters (Sun-Sat), separated by a space.")
      days = input().split()

      for day in days:
        week[day.capitalize()].append(event)
    return week # Return the updated week
  except ValueError:
    print("Invalid input. Please try again.")
    add_event(week)

# Function to print the week
def show_week(week):
  for day in week:
    print(day)
    for event in week[day]:
      print("\n" + str(event))
    print("------------------------------")

# Function to find openings in schdule
def find_openings(week):
  print("In minutes, what would you like the check interval to be?")
  print("(leave blank to default to 15 or type 'info' for an explantion)")
  check_interval = input()

  # More info
  if check_interval == "info":
    print("The check interval is the amount of time between each check for openings.")
    print("\n For example, if the check interval is 15, then the program will check for openings every 15 minutes.")
    print("\n This means that if there is an event that starts at 9:00 am and ends at 10:10 am, the first available time would be 10:15 am.")
    find_openings(week)

  else:
    try:
      time_hold =[]
      check_interval = int((15/60) * 100) if check_interval == "" else int((int(check_interval)/60) * 100)

      for day in week:
        time_hold.clear()
        insert_count = 0

        # No events means everyone is free
        if len(week[day]) == 0:
          opening = Event("Opening", 0.0, 23.75, "")
          week[day].insert(0, opening)
          
        for event in week[day]:
          # Checks for openings
          for time in range(0, 2400, check_interval):
            if time not in range(int(event.start_time * 100), int(event.end_time * 100)):
              time_hold.append ((float(time) / 100))
              
        # Create new events for openings
        for i in range(len(time_hold) - 1):
          # If before another event, insert before
          if time_hold[i] + 0.5 < time_hold[i + 1]:
            opening = Event("Opening", time_hold[0], time_hold[i], "")
            week[day].insert(0 + insert_count, opening)
            insert_count += 1
            time_hold[0] = time_hold[i + 1]

          # After all events
          elif time_hold[i + 1] == 23.75:
            opening = Event("Opening", time_hold[0], time_hold[i + 1], "")
            week[day].append(opening)

            # Update next starting value
            time_hold[0] = time_hold[i + 1]
        
    except ValueError:
      print("Invalid input")
      find_openings(week)

  return week


# Function to delete all events from the week
def delete_all_events(week):
  print("Are you sure you want to delete all events? (y/n)") # Can't be too careful
  answer = input().lower()
  if answer == "y":
    new_week = {"Sun": [],
                "Mon": [],
                "Tue": [],
                "Wed": [],
                "Thu": [],
                "Fri": [],
                "Sat": []}
    return new_week # Returns a new week with all events deleted
  else:
    return week # Returns the original week


# Main function
def main():
  cont = True
  week = {"Sun": [],
          "Mon": [],
          "Tue": [],
          "Wed": [],
          "Thu": [],
          "Fri": [],
          "Sat": []}
  
  while cont:
    print_menu()
    option = input()
    if option == "1":
      week = delete_openings(week)
      add_event(week)
    elif option == "2":
      show_week(week)
    elif option == "3":
      week = delete_openings(week)
      find_openings(week)
    elif option == "4":
      week = delete_all_events(week)
    elif option == "-1":
      cont = False
    else:
      print("Invalid option")

if __name__ == "__main__":
  main()