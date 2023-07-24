# This file contains all the elevator functions

from elevator.models import Elevator, ElevatorStatus
import time

def move_elevator(elevator_id):
    """
    This function moves the elevator to the destination floor
    """
    elevator = Elevator.objects.get(id=elevator_id)
    if elevator.direction:
        while elevator.current_floor < elevator.destination_floor:
            elevator = Elevator.objects.get(id=elevator_id)
            elevator.current_floor += 1
            elevator.save()
            time.sleep(0.1)
    else:
        while elevator.current_floor > elevator.destination_floor:
            elevator = Elevator.objects.get(id=elevator_id)
            elevator.current_floor -= 1
            elevator.save()
            time.sleep(0.1)
    elevator.destination_floor = None
    elevator.status = ElevatorStatus.objects.get(status="idle")
    elevator.save()
    

def on_called(elevator_id, current_floor, destination_floor):
        """
        This is called when somebody presses the up or down button to call the elevator.
        This could happen at any time, whether or not the elevator is moving.
        The elevator could be requested at any floor at any time, going in either direction.
        elevator_id: the id of the elevator that the user intends to use
        current_floor: the floor that the elevator is being called to
        destination_floor: the destination floor the caller wants to go to
        """
        elevator = Elevator.objects.get(id=elevator_id)
        if elevator.status == None:
            return "This elevator is not working"
        if current_floor < elevator.min_floor or current_floor > elevator.max_floor:
            return "Current floor is not served by this elevator"
        if destination_floor < elevator.min_floor or destination_floor > elevator.max_floor:
            return "Destination floor is not served by this elevator"
        if elevator.status.status == "idle":
            call_when_idle(elevator_id, current_floor, destination_floor)
            move_elevator(elevator_id)
        elif elevator.status.status == "moving":
            while(elevator.direction != current_floor < destination_floor or elevator.status.status != "idle"):
                elevator = Elevator.objects.get(id=elevator_id)
                time.sleep(0.5)
            if elevator.status.status == "idle":
                call_when_idle(elevator_id, current_floor, destination_floor)
                move_elevator(elevator_id)
            elif elevator.destination_floor < destination_floor:
                elevator.destination_floor = destination_floor
                move_elevator(elevator_id)
        elevator = Elevator.objects.get(id=elevator_id)
        return f"Request completed, elevator is at {elevator.current_floor} floor, and status is {elevator.status.status}"

def call_when_idle(elevator_id, current_floor, destination_floor):
    """
    This is called when the elevator is idle.
    """
    elevator = Elevator.objects.get(id=elevator_id)
    if elevator.status.status == "idle":
        elevator.current_floor = current_floor
        elevator.destination_floor = destination_floor
        elevator.direction = current_floor < destination_floor
        elevator.status = ElevatorStatus.objects.get(status="moving")
        elevator.save()

def start_maintainence(elevator_id):
    """
    This is called when the elevator is in maintainence mode.
    """
    elevator = Elevator.objects.get(id=elevator_id)
    elevator.status = None
    elevator.save()
    return "Elevator is in maintainence mode"

def finish_maintainence(elevator_id):
    """
    This is called when the elevator is finished with maintainence mode.
    """
    elevator = Elevator.objects.get(id=elevator_id)
    elevator.current_floor = elevator.min_floor
    elevator.destination_floor = None
    elevator.direction = None
    elevator.status = ElevatorStatus.objects.get(status="idle")
    elevator.save()
    return "Maintainence complete, elevator is ready to use"