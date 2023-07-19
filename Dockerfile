FROM python
WORKDIR /app/mob
ADD . .
RUN pip install aiogram
CMD ["python", "bot.py"]