FROM ruby:2.4.1

RUN apt-get update
RUN apt-get install nodejs -y

RUN mkdir /myapp
WORKDIR /myapp
COPY . /myapp/

RUN bundle install
RUN bin/rails db:environment:set RAILS_ENV=development
RUN bin/rails db:migrate RAILS_ENV=development

# RUN rake db:schema:load RAILS_ENV=development --trace
# RUN rake db:schema:load --trace