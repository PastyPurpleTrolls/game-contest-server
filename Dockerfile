FROM ruby:2.4.1

RUN apt-get update
RUN apt-get install -y nodejs build-essential python3.4 gcc

COPY Gemfile* /tmp/
WORKDIR /tmp
RUN gem install bundler && bundle install

RUN mkdir /myapp
WORKDIR /myapp
COPY . /myapp/

ENV RAILS_ENV development

CMD ["bash", "-c", "cp /myapp/examples/guess-w/ref_helper.py /usr/lib/python3.4/;clockworkd -d . start ./clock.rb --log;bin/rails db:migrate; bin/rake db:seed; bin/rails s -b 0.0.0.0"]
