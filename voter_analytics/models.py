# voter_analytics/models.py
import csv
from django.db import models
from django.urls import reverse

class Voter(models.Model):
    '''Model for a registered voter'''
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    street_number = models.CharField(max_length=10)
    street_name = models.CharField(max_length=100)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    zip_code = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=50)
    precinct_number = models.CharField(max_length=10)
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    voter_score = models.IntegerField()

    def __str__(self):
        '''String representation of a voter'''
        return f"{self.first_name} {self.last_name} ({self.party_affiliation})"

    def get_absolute_url(self):
        '''URL for viewing a voter'''
        return reverse('voter_detail', args=[str(self.id)])
    
    @classmethod
    def load_data(cls, file_path='newton_voters.csv'):
        '''Load voter data from a CSV file'''
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            voters = []
            for row in reader:
                v20state = row['v20state'].strip().lower() == 'true'
                v21town = row['v21town'].strip().lower() == 'true'
                v21primary = row['v21primary'].strip().lower() == 'true'
                v22general = row['v22general'].strip().lower() == 'true'
                v23town = row['v23town'].strip().lower() == 'true'
                voter = cls(
                    first_name=row['First Name'],
                    last_name=row['Last Name'],
                    street_number=row['Residential Address - Street Number'],
                    street_name=row['Residential Address - Street Name'],
                    apartment_number=row.get('Residential Address - Apartment Number', ''),
                    zip_code=row['Residential Address - Zip Code'],
                    date_of_birth=row['Date of Birth'],
                    date_of_registration=row['Date of Registration'],
                    party_affiliation=row['Party Affiliation'].strip(),
                    precinct_number=row['Precinct Number'],
                    v20state=v20state,
                    v21town=v21town,
                    v21primary=v21primary,
                    v22general=v22general,
                    v23town=v23town,
                    voter_score=int(row['voter_score'])
                )
                voters.append(voter)
            cls.objects.bulk_create(voters)
                
                
