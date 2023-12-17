FROM python:3.11.5

WORKDIR /lorenzo-search

COPY requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

EXPOSE 8080

COPY . /lorenzo-search

ENTRYPOINT ["streamlit", "run"]

CMD ["dev_search.py"]