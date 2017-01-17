def login(user, options = {})
  if options[:avoid_capybara]
    post sessions_path, username: user.username, password: user.password
  else
    visit login_path
    fill_in 'Username', with: user.username
    fill_in 'Password', with: user.password
    click_button 'Log In'
  end
end

shared_examples "redirects to a login" do |options|
  options ||= {}

  unless options[:skip_browser]
    describe "visit browser path" do
      before { visit path }

      it { should have_alert(:warning) }
      it { should have_content('Login') }
    end
  end

  unless options[:browser_only]
		describe "visit HTTP path", type: :request do
 	  	before { send(method, http_path) }

 	   	it { errors_on_redirect(login_path, :warning) }
 	 	end
	end
end

shared_examples "redirects to root" do |options|
  options ||= {}

  describe "requesting", type: :request do
    before { login login_user, avoid_capybara: true }

    unless options[:skip_browser]
      describe "visit browser path" do
        before { get path }

        specify { expect(response.body).not_to match(signature) }
        it { errors_on_redirect(root_path, error_type) }
      end
    end

  	unless options[:browser_only]
    	describe "visit HTTP path" do
      	before { send(method, http_path) }

      	it { errors_on_redirect(root_path, error_type) }
    	end
		end
  end
end
