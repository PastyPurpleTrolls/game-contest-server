require 'fileutils'
require 'shellwords'

module Uploadable
  extend ActiveSupport::Concern

  included do
    before_destroy :delete_code_locations
    validate :file_location_exists
  end

  # For referees - referee file
  # For players - player file
  def upload=(uploaded_io)
    unless self.name.blank?
      location_data = store_file(uploaded_io, self.class.to_s.downcase.pluralize)
      copy_player_includes_to_player(location_data[:file]) if self.class == Player
      copy_logs(self.file_location, location_data[:directory])
      delete_code(self.file_location)
      self.file_location = location_data[:file]
    end
  end

  # For referees - player-includes file
  def upload2=(uploaded_io)
    unless self.name.blank?
      delete_code(self.compressed_file_location)
      location_data = store_file(uploaded_io, 'environments')
      self.compressed_file_location = location_data[:file]
    end
  end

  # For referees - replay plugin file
  def upload3=(uploaded_io)
    unless self.name.blank?
      delete_code(self.replay_assets_location)
      new_directory = File.join("static", self.class.to_s.downcase.pluralize)
      location_data = store_file(uploaded_io, new_directory)
      self.replay_assets_location = location_data[:directory]
    end
  end

  def file_location_exists
    if self.file_location.nil? || !File.exists?(self.file_location)
      errors.add(:file_location, "doesn't exist on the server")
    end
  end

  private

  def copy_player_includes_to_player(player_location)
    player_includes_location = self.contest.referee.compressed_file_location
    player_directory = File.dirname(player_location)
    uncompress(player_includes_location, player_directory)
    FileUtils.cp(player_includes_location, player_directory)
  end

  def copy_logs(old_directory, new_directory)
    old_log_directory = "#{old_directory}/logs"
    new_log_directory = "#{new_directory}/logs"
    FileUtils.mkdir_p new_log_directory
    if File.exist?(old_log_directory)
      FileUtils.cp("#{old_log_directory}/*", new_log_directory)
      self.update_log_locations new_directory
    end
  end

  def delete_code_locations
    delete_code(self.file_location)
    delete_code(self.compressed_file_location) if self.has_attribute?(:compressed_file_location)
    delete_code(self.replay_assets_location) if self.has_attribute?(:replay_assets_location)
  end

  # Delete directory where file is located
  def delete_code(location)
    unless location.nil?
      pathname = Pathname.new(location)
      unless pathname.directory?
        location = pathname.dirname
      end
      FileUtils.rm_rf(location) if pathname.exist?
      if pathname.exist?
        raise "Deleting stuff it shouldnt"
      end
    end
  end

  def store_file(uploaded_io, dir)
    file_location = ''
    dir_location = ''
    unless uploaded_io.nil?
      dir_location = Rails.root.join('code', dir, Rails.env, random_hex)
      file_location = dir_location.join(uploaded_io.original_filename).to_s
      dir_location = dir_location.to_s
      FileUtils.mkdir_p dir_location
      IO.copy_stream(uploaded_io, file_location)
      uncompress(file_location, dir_location)
    end
    {file: file_location, directory: dir_location}
  end

  def uncompress(src, dest)
    safe_src = Shellwords.escape src
    safe_dest = Shellwords.escape dest
    safe_dest_files = Dir.glob "#{safe_dest}/*"
    system("tar -xvf #{safe_src} -C #{safe_dest} > /dev/null 2>&1")
    system("unzip -o #{safe_src} -d #{safe_dest} > /dev/null 2>&1")
    mark_as_executable safe_dest_files
    system("dos2unix -q #{safe_dest_files}")
  end

  def mark_as_executable(file)
    FileUtils.chmod('+x', file)
  end

  def random_hex
    SecureRandom.hex
  end
end

