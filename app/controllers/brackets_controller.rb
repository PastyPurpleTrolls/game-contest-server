class BracketsController < ApplicationController
  def show
    tid = params[:id]
    puts tid.to_s
    render json: {id: tid}
  end

  private
  def ...
  end
end