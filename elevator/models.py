from django.db import models

class ElevatorStatus(models.Model):
    status = models.CharField(max_length=20, null=False)  

    def __str__(self):
        return f"{self.id}: {self.status}" 

    class Meta:
        db_table = 'elevator_status'

class Elevator(models.Model):
    id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=50, null=True)  
    status = models.ForeignKey(ElevatorStatus, on_delete=models.CASCADE, null=True)
    current_floor = models.IntegerField(null=False)
    destination_floor = models.IntegerField(null=True, blank=True)
    moving_up = models.BooleanField(null=True, blank=True)  # True if going up, False if going down.
    min_floor = models.IntegerField(null=False, blank=False)  
    max_floor = models.IntegerField(null=False, blank=False)  
    max_capacity = models.IntegerField(null=False)  # max no. of people that the elevator carry safely
    current_capacity = models.IntegerField(null=True)  # current no. of people inside the elevator
    door_close= models.BooleanField(default=True)  # True if door is closed, False if door is open
    
    def __str__(self):
        return f"{self.id}"

    def open_door(self):
        if not self.door_close:
            raise ValueError('The door should be closed before the lift get started.')
        self.door_close= False
        self.save()
        
    def close_door(self):
        if self.door_close:
            raise ValueError('The door is already closed.')
        self.door_close= True
        self.save()    
          
    class Meta:
        db_table = 'elevator'
