from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render,get_object_or_404,redirect
from django.http import Http404
from .models import BlogPost
from .forms import BlogPostModelForm
# Create your views here.

def blog_post_detail_page(request,slug):
    print("Django says",request.method,request.path,request.user)
    # queryset=BlogPost.objects.filter(slug=slug)
    obj=get_object_or_404(BlogPost,slug=slug)
    # if queryset.count() >=1:
    #     obj=queryset.first()
    #    raise Http404
    # if queryset.count()==0:
    #     raise Http404
    # obj=queryset.first()
   
    template_name="blog_post_detail.html"
    context={"title":obj.title,"content":obj.content}
    # context={"object":obj}
    print(context)
    return render(request,template_name,context)

# def blog_post_detail_page(request,post_id): 
#     # obj=BlogPost.objects.get(id=1)
#     print(post_id.__class__)
#     obj=get_object_or_404(BlogPost,post_id)
#     # try:
#     #  obj=BlogPost.objects.get(id=post_id)
#     #  print(obj)
#     # except BlogPost.DoesNotExist:
#     #     raise Http404
#     # except ValueError:
#     #     raise Http404
#     template_name="blog_post_detail.html"
#     context={"title":obj.title,"content":obj.content}
#     # context={"object":obj}
#     print(context)
#     return render(request,template_name,context)

#CRUD 
#CREATE RETRIEVE UPDATE DELETE
#GET -Retrieve/List
#POST -create/update/delete

def blog_post_list_view(request):
    #list out objects
    #could be search
    qs=BlogPost.objects.all()
    # qs=BlogPost.objects.filter(title__icontains="NEW")
    # qs=BlogPost.objects.filter(title__icontains="MY")
    template_name='blog/list.html'
    context={"objects_list":qs}
    return render(request,template_name,context)

@staff_member_required #if user is not login into django then it directly show the login admin panel after that show that view form ..here create_view form
# @login_required(login_url='\login')used with useer is not login then the create view form is not diplay it get oage not found error.
def blog_post_create_view(request):
    #create object
    #? use a form
    form=BlogPostModelForm(request.POST or None)
    if form.is_valid():
        obj=form.save(commit=False)
        obj.user=request.user
        form.save()
        form=BlogPostModelForm()
    template_name="form.html"
    context={"form":form}
    return render(request,template_name,context)

        # print(form.cleaned_data)
        # title=form.cleaned_data['title']
        # obj=BlogPost.objects.create(**form.cleaned_data)

def blog_post_details_view(request,slug):
    #retrieve 1 object->detail view
    obj=get_object_or_404(BlogPost,slug=slug)
    template_name="blog/detail.html"
    context={"title":obj.title}
    return render(request,template_name,context)

@staff_member_required
def blog_post_update_view(request,slug):
    obj=get_object_or_404(BlogPost,slug=slug)
    form=BlogPostModelForm(request.POST or None,instance=obj)
    if form.is_valid():
        form.save()
    template_name="form.html"
    context={"form":form, "title":f"update{obj.title}"}
    # template_name="blog/update.html"
    # context={"object":obj.title,"form":None}
    return render(request,template_name,context)

@staff_member_required
def blog_post_delete_view(request,slug):
    obj=get_object_or_404(BlogPost,slug=slug)
    template_name="blog/delete.html"
    if request.method=='POST':
        obj.delete()
        return redirect("/")
    context={"title":obj.title}
    return render(request,template_name,context)
