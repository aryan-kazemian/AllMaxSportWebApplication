from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Ticket, Message
from .serializers import TicketSerializer, MessageSerializer

class TicketView(APIView):
    def get(self, request, *args, **kwargs):
        filters = {}
        for field in ['id', 'status', 'priority', 'related_order_id', 'customer_id', 'created_at']:
            val = request.query_params.get(field)
            if val:
                filters[field if field != 'id' else 'pk'] = val

        tickets = Ticket.objects.filter(**filters) if filters else Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        ticket_id = request.query_params.get('id')

        if ticket_id:
            ticket = get_object_or_404(Ticket, pk=ticket_id)
            serializer = MessageSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(ticket=ticket)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        ticket_id = request.query_params.get('id')
        message_id = request.query_params.get('message_id')

        if ticket_id:
            ticket = get_object_or_404(Ticket, pk=ticket_id)
            serializer = TicketSerializer(ticket, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if message_id:
            message = get_object_or_404(Message, pk=message_id)
            serializer = MessageSerializer(message, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Missing id or message_id"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        ticket_id = request.query_params.get('id')
        message_id = request.query_params.get('message_id')

        if ticket_id:
            ticket = get_object_or_404(Ticket, pk=ticket_id)
            ticket.delete()
            return Response({"message": "Ticket deleted"}, status=status.HTTP_200_OK)

        if message_id:
            message = get_object_or_404(Message, pk=message_id)
            message.delete()
            return Response({"message": "Message deleted"}, status=status.HTTP_200_OK)

        return Response({"error": "Missing id or message_id"}, status=status.HTTP_400_BAD_REQUEST)
