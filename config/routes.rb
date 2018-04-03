GameContestServer::Application.routes.draw do
  get "visual_tests/colorscheme", as: :colorscheme
  root 'users#home'

  get '/help/', to: 'help#index'
  get '/help/terminology', to: 'help#terminology'
  get '/help/deleting_users', to: 'help#deleting_users'
  get '/help/changing_user_roles', to: 'help#changing_user_roles'
  get '/help/erd', to: 'help#erd'
  get '/help/manually_running_match', to: 'help#manually_running_match'
  get '/help/create_modify_referees', to: 'help#create_modify_referees'
  get '/help/create_modify_contests', to: 'help#create_modify_contests'
  get '/help/create_modify_tournaments', to: 'help#create_modify_tournaments'
  get '/help/writing_referee', to: 'help#writing_referee'
  get '/help/writing_replay_plugin', to: 'help#writing_replay_plugin'
  get '/help/upload_players_to_contest', to: 'help#upload_players_to_contest'
  get '/help/challenge_other_players', to: 'help#challenge_other_players'
  get '/help/view_results', to: 'help#view_results'

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
