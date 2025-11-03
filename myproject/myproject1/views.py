# myproject/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .api import get_orders, get_order, create_order, update_order, delete_order
from .forms import OrderForm

def show_orders(request):
    try:
        data = get_orders()
    except Exception as e:
        messages.error(request, f"Error consultando API: {e}")
        data = []
    return render(request, "show.html", {"obj": data})

def orders_new(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            payload = form.cleaned_data.copy()
            # asegurar tipos para el backend
            try:
                if "oid" in payload:
                    payload["oid"] = int(payload["oid"])
                if "price" in payload:
                    payload["price"] = float(payload["price"])
            except Exception:
                pass

            try:
                create_order(payload)  # envía: oid, fname, lname, price, mail, addr
                messages.success(request, "Orden creada.")
                return redirect("orders_show")
            except Exception as e:
                # intenta extraer detalle del API si viene en JSON
                detail = getattr(getattr(e, "response", None), "text", str(e))
                messages.error(request, f"Error creando: {detail}")
    else:
        form = OrderForm()
    return render(request, "orders.html", {"form": form})


def orders_edit(request, oid: int):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            payload = form.cleaned_data
            try:
                update_order(oid, payload)
                messages.success(request, "Orden actualizada.")
                return redirect("orders_show")
            except Exception as e:
                messages.error(request, f"Error actualizando: {e}")
    else:
        # precargar para el form
        try:
            current = get_order(oid)
            form = OrderForm(initial=current)
        except Exception as e:
            messages.error(request, f"No se pudo cargar la orden: {e}")
            return redirect("orders_show")
    return render(request, "orders.html", {"form": form, "edit": True, "oid": oid})

def orders_delete(request, oid: int):
    if request.method == "POST":   # por seguridad, borrar con POST
        try:
            delete_order(oid)
            messages.success(request, "Orden eliminada.")
        except Exception as e:
            messages.error(request, f"Error eliminando: {e}")
    return redirect("orders_show")

