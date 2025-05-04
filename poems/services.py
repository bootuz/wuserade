import datetime
from django.utils import timezone
from django.db.models import Q

from .models import Poem, FeaturedPoem


class FeaturedPoemService:
    """Service for managing featured poems"""
    
    @staticmethod
    def get_todays_featured_poem():
        """
        Get or create today's featured poem
        
        Returns:
            FeaturedPoem: The featured poem for today
        """
        today = timezone.now().date()
        
        # First try to get an existing featured poem for today
        featured = FeaturedPoem.objects.get_for_date(today)
        if featured:
            return featured
            
        # Create a new featured poem for today
        return FeaturedPoemService._create_featured_poem(today)
    
    @staticmethod
    def _create_featured_poem(date):
        """
        Create a new featured poem for the given date
        
        Args:
            date: The date to create a featured poem for
            
        Returns:
            FeaturedPoem: The newly created featured poem
            
        Raises:
            ValueError: If no eligible poems are available
        """
        # Find the most recent featured poem (for avoiding repetition)
        last_featured = FeaturedPoem.objects.get_latest()
        
        # Build an exclusion query for poems we don't want to feature
        exclusion_query = Q()
        
        # Don't repeat yesterday's poem
        yesterday = date - datetime.timedelta(days=1)
        if last_featured and last_featured.featured_date == yesterday:
            exclusion_query |= Q(id=last_featured.poem_id)
        
        # Get eligible poems
        eligible_poems = Poem.objects.exclude(exclusion_query)
        
        # Ensure we have poems to choose from
        poem_count = eligible_poems.count()
        if poem_count == 0:
            # Fallback: if all poems have been excluded, but we need one, just use any poem
            eligible_poems = Poem.objects.all()
            poem_count = eligible_poems.count()
            
            if poem_count == 0:
                raise ValueError("No poems available in the system")
        
        # Get a random poem - use offset for better performance than order_by('?')
        import random
        random_index = random.randint(0, poem_count - 1)
        random_poem = eligible_poems.select_related('author', 'category')[random_index]
        
        # Create and return the new featured poem
        return FeaturedPoem.objects.create(
            poem=random_poem,
            featured_date=date
        ) 
