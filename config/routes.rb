GameContestServer::Application.routes.draw do
  get "visual_tests/colorscheme", as: :colorscheme
  root 'users#home'

  get '/help/', to: 'help#index'
  get '/help/terminology', to: 'help#terminology'
  get '/help/erd', to: 'help#erd'
  get '/match_logs/:id/std_out', to: 'match_log_infos#std_out'
  get '/match_logs/:id/std_err', to: 'match_log_infos#std_err'
  
  resources :users
  resources :brackets, only: [:show]
  
  resources :referees do
    member do
      get 'assets/:asset', to: 'referees#show', :constraints => { :asset => /.*/ }, as: 'assets'
    end
  end
  
  resources :contests, shallow: true do
    resources :matches, except: [:edit, :update, :index] do
      resources :rounds, only: [:show]
    end
    resources :players, except: :index
    resources :tournaments, except: :index, shallow: true do
      resources :players, except: :index
    end
  end

  resources :sessions, only: [:new, :create, :destroy]
  
  get 'signup', to: 'users#new', as: :signup
  get 'login', to: 'sessions#new', as: :login
  delete 'logout', to: 'sessions#destroy', as: :logout
end
