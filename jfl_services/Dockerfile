FROM python

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
#RUN python db/jfl_db.py --populate

EXPOSE 5000
CMD python run.py
