import json
from rest_framework import viewsets
from elevator import models, serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from elevator import utils


class ElevatorViewSet(viewsets.ModelViewSet):
    """
    As we need to perform standard CRUD operations on the Elevator model, we are using ModelViewSet
    """
    queryset = models.Elevator.objects.all()
    serializer_class = serializers.ElevatorSerializer


@api_view(["POST"])
def use_elevator(request):
    """
    Handles the user requests to use the elevator
    """
    if request.method == 'POST':
        payload = json.loads(request.body.decode('utf-8')) # JSON data is stored into a Python dictionary
        elevator_id = payload.get('elevator_id') # code tries to extract the 'elevator_id' from the payload
        if str(elevator_id).isnumeric():
            elevator_name = payload.get('elevator_name') # user can also pass the name of the elevator
            if elevator_name is not None:
                elevator = models.Elevator.objects.get(name=elevator_name)
                if elevator is not None:
                    elevator_id = elevator.id
        current_floor = payload.get('current_floor')
        destination_floor = payload.get('destination_floor')
        try:
            elevator_id = int(elevator_id)
            current_floor = int(current_floor)
            destination_floor = int(destination_floor)
        except Exception as e:
            return Response({'error': 'Missing or bad parameters'}, status=status.HTTP_400_BAD_REQUEST)

        request_status = utils.on_called(elevator_id, current_floor, destination_floor)
        payload = {
            'elevator_id': elevator_id,
            'request_status': request_status
        }
        return Response(payload,status=status.HTTP_200_OK)
    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["POST"])
def elevator_maintainence(request):
    """
    Handles maintainence requests for the elevator
    """
    if request.method == 'POST':
        payload = json.loads(request.body.decode('utf-8'))
        elevator_id = payload.get('elevator_id')
        action = payload.get('action')
        if str(elevator_id).isnumeric():
            elevator_name = payload.get('elevator_name') # user can also pass the name of the elevator
            if elevator_name is not None:
                elevator = models.Elevator.objects.get(name=elevator_name)
                elevator_id = elevator.id
        if action == 'start':
            request_status = utils.start_maintainence(elevator_id)
            return_payload = {
                'elevator_id': elevator_id,
                'request_status': request_status
            }
            return Response(return_payload,status=status.HTTP_200_OK)
        elif action == 'finish':
            request_status = utils.finish_maintainence(elevator_id)
            return_payload = {
                'elevator_id': elevator_id,
                'request_status': request_status
            }
            return Response(return_payload,status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Missing or bad parameters'}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
