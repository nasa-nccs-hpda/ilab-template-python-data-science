FROM python:3.11-slim-bullseye

ENV DEBIAN_FRONTEND=noninteractive
ENV HF_HUB_DISABLE_PROGRESS_BARS=1

RUN rm -rf /etc/apt/sources.list.d/*.list && \
    apt-get update && apt-get install -y git gcc build-essential python3-dev libgeos-dev

RUN python3 -m pip install --upgrade pip setuptools wheel

COPY requirements.txt .
RUN python3 -m pip install --upgrade pip setuptools wheel cython numpy pyshp six pyproj streamlit-folium
RUN python3 -m pip install --upgrade --no-binary :all: shapely
RUN python3 -m pip install git+https://github.com/SciTools/cartopy.git --upgrade cartopy

RUN python3 -m pip install --no-cache-dir --compile -r requirements.txt

RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME

RUN mkdir ./pages
COPY --chown=user /pages ./pages

EXPOSE 7860

CMD ["streamlit", "run", "./pages/Home.py", "--server.port=7860"]