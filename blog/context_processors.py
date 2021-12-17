from .models import Tag

def article_tag(request):
	tags = Tag.objects.all()
	return {"tags":tags}