from django.views.generic import ListView, DetailView
#from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import UpdateView, DeleteView,CreateView,FormView
from .models import Articulo
from django.urls import reverse_lazy,reverse #modificada
from .forms import FormularioComentario
from django.views import View #movida
from django.views.generic.detail import SingleObjectMixin  #nueva
from .models import Articulo
from .forms import FormularioComentario
#from paypal.standard.forms import PayPalPaymetsForm
from django.conf import settings
import uuid
from django.shortcuts import render

# Create your views here.

#lista por artista
# class VistaListaArticulosArtista(ListView):
#     model = Articulo
#     template_name = 'lista_articulos_artistas.html'
#     context_object_name = 'articulo_list'

#     def get_queryset(self):
#         # Obtén el parámetro de la URL llamado 'genero'
#         artista = self.kwargs.get('artista', None)

#         # Filtra los artículos por género si se proporciona el parámetro, de lo contrario, devuelve todos los artículos
#         if artista:
#             return Articulo.objects.filter(artista=artista)
#         else:
#             return Articulo.objects.all()
def es_administrador(user):
    return user.is_authenticated and user.is_staff


#lista por genero
class VistaListaArticulos(ListView):
    model = Articulo
    template_name = 'lista_articulos.html'
    context_object_name = 'articulo_list'

    def get_queryset(self):
        # Obtén el parámetro de la URL llamado 'genero'
        genero = self.kwargs.get('genero', None)

        # Filtra los artículos por género si se proporciona el parámetro, de lo contrario, devuelve todos los artículos
        if genero:
            return Articulo.objects.filter(genero=genero)
        else:
            return Articulo.objects.all()

        
class VistaListaArticulosPorCategoria(ListView):
    model = Articulo
    template_name = 'lista_articulos_por_categoria.html'
    context_object_name = 'articulo_list'

    def get_queryset(self):
        # Obtén el parámetro de la URL llamado 'categoria'
        categoria = self.kwargs.get('categoria', None)

        # Filtra los artículos por categoría si se proporciona el parámetro, de lo contrario, devuelve todos los artículos
        if categoria:
            return Articulo.objects.filter(categoria=categoria)
        else:
            return Articulo.objects.all()

        
        
class VistaListaCategorias(ListView):
    model = Articulo
    template_name = 'lista_categorias.html'  # Crea este template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Articulo.objects.values_list('categoria', flat=True).distinct()
        return context
# class VistaListaCategoriasArtistas(ListView):
#     model = Articulo
#     template_name = 'lista_categorias.html'  # Crea este template

#     def get_context_data2(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['artistas'] = Articulo.objects.values_list('artista', flat=True).distinct()
#         return context
    
class VistaDetalleArticulo(DetailView):
    model = Articulo
    template_name='detalle_articulo.html'
    def get(self,request,*args,**kwargs):
        view=ComentarioGet.as_view()
        return view(request,*args,**kwargs)
    def post(self,request,*args,**kwargs):
        view=ComentarioPost.as_view()
        return view(request,*args,**kwargs)
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     article = self.get_object()

    #     host = self.request.get_host()


@method_decorator(user_passes_test(es_administrador), name='dispatch')
class VistaModificacionArticulo(UpdateView):
    model=Articulo
    fields=(
        'artista',
        'titulo',
        'cuerpo',
        'genero',
        'categoria',
        'costo',
        'imagen',
        'tracklist',
        'fecha_creacion'
    )
    template_name='editar_articulo.html'
    success_url=reverse_lazy('lista_articulos')

@method_decorator(user_passes_test(es_administrador), name='dispatch')
class VistaEliminacionArticulo(DeleteView): 
    model = Articulo
    template_name= 'eliminar_articulo.html'
    success_url=reverse_lazy('lista_articulos')
    object_name = 'articulo'
@method_decorator(user_passes_test(es_administrador), name='dispatch')
class VistaCrearArticulo(CreateView):
        model=Articulo
        template_name='nuevo_articulo.html'
        fields=(
            'artista',
             'titulo',
             'cuerpo',
              'genero',
              'categoria',
              'costo',
              'imagen',
              'tracklist',
              'fecha_creacion',
        )
        success_url=reverse_lazy('lista_articulos')
        
        
        def form_valid(self, form): 
          #  form.instance.id = uuid.uuid4()
            form.instance.autor = self.request.user
            return super().form_valid(form)
        
#@method_decorator(login_required, name='dispatch')
class ComentarioGet(DetailView):
     model=Articulo
     template_name='detalle_articulo.html'
     def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        #context['form']=FormularioComentario
        context['form'] = FormularioComentario(usuario_autenticado = self.request.user)
        return context


#@method_decorator(login_required, name='dispatch')
class ComentarioPost(SingleObjectMixin,FormView,View):
    model=Articulo
    form_class = FormularioComentario
    template_name = 'detalle_articulo.html'

    def post(self,request,*args, **kwargs):
        self.Articulo=self.get_object()
        #form=self.get_form()
        return super().post(request,*args,**kwargs) 
    
    def form_valid(self,form):
        #comentario=self.form_get()
        comentario=form.save(commit=False)
        comentario.Articulo=self.Articulo
        comentario.autor = self.request.user # establece el autor como el usuario autenticado
        comentario.save()
        return super().form_valid(form)

    def get_success_url(self):
        articulo=self.get_object()
        return reverse('detalle_articulo',kwargs={'pk':articulo.pk})
