from django.db.models import Q

# Example user input
search_query = "hello world"
words = search_query.strip().split()

# Build a Q object for each word
query = Q()
for word in words:
    query &= Q(title__icontains=word)

# Apply the filter
results = Entry.objects.filter(
    query,
    creation_date__date__gte=self.from_date,
    creation_date__date__lte=self.to_date
)


# Yes — you're on the right track, but Django's icontains only checks for one substring, and doesn't support multiple word searches out-of-the-box unless they appear exactly like in your search string.

# If the user enters multiple space-separated words like "hello world", and you want to check whether each of those words individually appears somewhere in the field (non-consecutively) 
# — like "Hello, beautiful, amazing world" — then you need to split the string and build multiple Q objects combined with & (AND) for filtering.
