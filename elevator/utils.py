# This file contains all the elevator functions

from elevator.models import Elevator, ElevatorStatus
import time

def move_elevator(elevator_id):
    """
    This function moves the elevator to the destination floor
    """
    elevator = Elevator.objects.get(id=elevator_id)
    if elevator.moving_up:
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
        The elevator can be requested from any floor and going in any direction (up or down). .
        The user specifies the elevator_id, current_floor, and destination_floor."
        """
        elevator = Elevator.objects.get(id=elevator_id)
        if elevator.status == None:
            return "This elevator is not working, it is under maintenance mode"
        if current_floor < elevator.min_floor or current_floor > elevator.max_floor:
            return "Current floor is not served by this elevator"
        if destination_floor < elevator.min_floor or destination_floor > elevator.max_floor:
            return "Destination floor is not served by this elevator"
        if elevator.status.status == "idle":
            call_when_idle(elevator_id, current_floor, destination_floor)
            move_elevator(elevator_id)
        elif elevator.status.status == "moving":
            while(elevator.moving_up != current_floor < destination_floor or elevator.status.status != "idle"):
                elevator = Elevator.objects.get(id=elevator_id)
                time.sleep(0.5)
            if elevator.status.status == "idle":
                call_when_idle(elevator_id, current_floor, destination_floor)
                move_elevator(elevator_id)
            elif elevator.destination_floor < destination_floor:
                elevator.destination_floor = destination_floor
                move_elevator(elevator_id)
        elevator = Elevator.objects.get(id=elevator_id)
        return f"Your request has been granted and the elevator has moved to the {elevator.current_floor} floor, and status is '{elevator.status.status}'"

def call_when_idle(elevator_id, current_floor, destination_floor):
    """
    This is called when the elevator is idle.
    """
    elevator = Elevator.objects.get(id=elevator_id)
    if elevator.status.status == "idle":
        elevator.current_floor = current_floor
        elevator.destination_floor = destination_floor
        elevator.moving_up = current_floor < destination_floor
        elevator.status = ElevatorStatus.objects.get(status="moving")
        elevator.save()

def start_maintenance(elevator_id):
    """
    This is called when the elevator is in maintenance mode.
    """
    elevator = Elevator.objects.get(id=elevator_id)
    elevator.status = None
    elevator.save()
    return "Elevator is in maintenance mode"

def finish_maintenance(elevator_id):
    """
    This is called when the elevator is finished with maintenance mode.
    """
    elevator = Elevator.objects.get(id=elevator_id)
    elevator.current_floor = elevator.min_floor
    elevator.destination_floor = None
    elevator.moving_up = None
    elevator.status = ElevatorStatus.objects.get(status="idle")
    elevator.save()
    return "maintenance complete, elevator is ready to use"