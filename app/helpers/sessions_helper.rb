module SessionsHelper
  def current_user
    @current_user ||= User.friendly.find(session[:user_id]) if session[:user_id]
  end

  def logged_in?
    !current_user.nil?
  end

  def current_user?(user)
    current_user == user
  end

  def login(user)
    session[:user_id] = user.id
  end

  def logout
    session[:user_id] = nil
  end

  def deny_access
    store_location
    flash[:warning] = "Access Denied"
    #redirect_to "/login"
    redirect_back_to_previous
  end

  def redirect_back_to_previous
    return_to = session[:return_to]
    clear_return_to
    redirect_to(return_to || root_path)
  end


  private

  def ensure_user_logged_in
    unless logged_in?
      flash[:warning] = 'Not logged in.'
      redirect_to login_path
    end
  end

  def ensure_user_logged_out
    unless !logged_in?
      flash[:warning] = 'You are already logged in.'
      redirect_to root_path
    end
  end

  def ensure_contest_creator
    unless current_user.contest_creator?
      flash[:danger] = 'Not a contest creator.'
      redirect_to root_path
    end
  end
	
	def ensure_correct_user_from_list(list_of_users, message)
    if !logged_in?
      flash[:warning] = 'Not logged in.'
      redirect_to login_path
    else
			unless list_of_users.include?(current_user)
      	flash[:danger] = message
      	redirect_to root_path
			end
    end
	end

  def ensure_correct_user(user_id = params[:id])
    @user = User.friendly.find(user_id)
    unless current_user?(@user) || current_user.admin?
      flash[:danger] = 'Unable to edit another user\'s stuff.'
      redirect_to root_path
    end
  end

  
  def store_location
    session[:return_to] = request.referrer
  end

  def clear_return_to
    session[:return_to] = nil
  end

end
