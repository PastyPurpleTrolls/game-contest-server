class ApplicationController < ActionController::Base
  # Prevent CSRF attacks by raising an exception.
  # For APIs, you may want to use :null_session instead.
  protect_from_forgery with: :exception
  before_action :get_daemon_status

  include SessionsHelper
	include MatchesHelper

  def get_daemon_status
    r, w = IO.pipe

    unless File.exist?("#{Rails.root}/tmp/clockworkd.clock.output")
      @daemon_status = false
      return
    end

    Process.wait get_expr_call(w)
    w.close
    access_time = r.read.to_i
    @daemon_status = access_time <= 15
  end

  def get_expr_call(w)
    if OS.mac?
      Process.spawn("expr $(gdate +%s) - $(gdate +%s -r #{Rails.root}/tmp/clockworkd.clock.output)", :out=>w)
    else
      Process.spawn("expr $(date +%s) - $(date +%s -r #{Rails.root}/tmp/clockworkd.clock.output)", :out=>w)
    end
  end
end
