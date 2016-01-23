class RefereesController < ApplicationController
    protect_from_forgery :except => :show
    before_action :ensure_user_logged_in, except: [:index, :show]
    before_action :ensure_contest_creator, except: [:index, :show]
    before_action :ensure_referee_owner, only: [:edit, :update, :destroy]

    def index
        @referees = Referee.search(params[:search]).paginate(:per_page => 10, :page => params[:page])
        if @referees.length == 0
            flash.now[:info] = "There were no referees that matched your search. Please try again!"
        end
    end

    def new
        @referee = Referee.new
    end

    def create
        @referee = current_user.referees.build(acceptable_params)
        if @referee.save
            flash[:success] = 'Referee created.'
            redirect_to @referee
        else
            render 'new'
        end
    end

    def edit
    end

    def update
        if @referee.update(acceptable_params)
            flash[:success] = 'Referee updated.'
            redirect_to @referee
        else
            render 'edit'
        end
    end

    def show
        @referee = Referee.friendly.find(params[:id])
        #GET param to grab an asset for the referee
        if params[:asset] 
            begin
                filename = File.join(@referee.replay_assets_location, params[:asset])
                send_file filename
            rescue
                raise ActionController::RoutingError.new('Not Found')
            end
            return
        end            
    end

    def destroy
        if ! Contest.exists?(:referee_id => @referee.id) 
            @referee.destroy
            flash[:success] = 'Referee deleted.'
            redirect_to referees_path
        else
            flash[:danger] = 'This referee is currently being used in a contest'
            render 'show'
        end
    end

		private

=begin
<<<<<<< HEAD
  def acceptable_params
    params.require(:referee).permit(:name,
                                    :rules_url,
				    :round_limit,
                                    :rounds_capable,
                                    :players_per_game,
				    :time_per_game,
                                    :upload,
				    :upload2)
  end
=======
    def acceptable_params
        params.require(:referee).permit(:name,
                                        :rules_url,
                                        :match_limit,
                                        :rounds_capable,
                                        :players_per_game,
                                        :time_per_game,
                                        :upload,
                                        :upload2,
                                        :upload3)
    end
>>>>>>> 2042a496d8a3de42ef23b5007c647a47bb77bb47
=end
    def acceptable_params
        params.require(:referee).permit(:name,
                                        :rules_url,
                                        :round_limit,
                                        :rounds_capable,
                                        :players_per_game,
                                        :time_per_game,
                                        :upload,
                                        :upload2,
                                        :upload3)
    end

    def ensure_referee_owner
        @referee = Referee.friendly.find(params[:id])
        ensure_correct_user(@referee.user_id)
    end


end
