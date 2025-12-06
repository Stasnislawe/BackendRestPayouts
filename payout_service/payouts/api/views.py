from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models.payout import Payout
from ..services.payout_services import PayoutService
from .serializers import PayoutSerializer


class PayoutViewSet(viewsets.ModelViewSet):
    queryset = Payout.objects.all()
    serializer_class = PayoutSerializer

    def create(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            payout = serializer.save()
            PayoutService.process_payout_async(str(payout.id))
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None) -> Response:
        payout = self.get_object()
        new_status = request.data.get('status')

        if not new_status:
            return Response(
                {'error': 'Статус обязателен'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            payout.status = new_status
            payout.save(update_fields=['status', 'updated_at'])
            serializer = self.get_serializer(payout)
            return Response(serializer.data)
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )