from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Review

#serializers with Model and views.

 #create and  update are provided, default fields are populated.
class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        exclude = ('watchlist',)
        #fields = "__all__"
        
class WatchListSerializer(serializers.ModelSerializer):
    #reviews = ReviewSerializer(many=True, read_only =True)
    platform = serializers.CharField(source = 'platform.name')
    class Meta:
        model = WatchList
        fields= "__all__"
 

class StreamPlatformSerializer(serializers.ModelSerializer):
    #watchlist = WatchListSerializer(many=True, read_only = True) by data
    #watchlist = serializers.StringRealatedField(many=True) by title 
    #watchlist = serializers.PrimaryKeyRelatedField(many=True, read_only=True) by pk
    
    watchlist = WatchListSerializer(many=True, read_only=True) 
    
    class Meta:
        model = StreamPlatform
        fields = "__all__"
        




#serializers with no Views.

#         #3.validators. OUR THIRD VALIDATION TYPE, individual fields.
# def validateActive(BooleanField):
#     if BooleanField is False:
#         raise serializers.ValidationError("Cannot be false")
    
# #serializer for our movie method and crud.
# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True) #read_only is a core field.
#     name = serializers.CharField()
#     description = serializers.CharField()
#     active = serializers.BooleanField(validators=[validateActive])
    
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data): #update our data of movies
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
    
#         #3 different types of validations in django
    
#         #1.field level validation. free level
#     def validate_name(self, value):
#         if len(value) < 2:
#             raise serializers.ValidationError("name is too short!")
#         else:
#             return value
        
#         #2. object level validation.
#     def validate(self, data):
#         if data ['name'] == data['description']:
#             raise serializers.ValidationError("Tittle and description cannot be same")
#         else:
#             return data


        
            


