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
      self.file_location = '' if self.file_location.nil?
      old_location = self.file_location
      location_data = store_file(uploaded_io, self.class.to_s.downcase.pluralize)
      self.file_location = location_data[:file]
      dir = location_data[:directory]
      FileUtils.mkdir_p "#{dir}/logs"

      if self.class == Player
        uncompress(self.contest.referee.compressed_file_location, File.dirname(self.file_location))
        FileUtils.cp(self.contest.referee.compressed_file_location, File.dirname(self.file_location))
      end

      old_dir = File.dirname(old_location)
      if File.exist?(old_dir + "/logs/")
        FileUtils.cp("#{old_dir}/logs/*", "#{dir}/logs/")
        self.update_log_locations self.file_location
      end
      delete_code(old_location)
    end
  end

  # For referees - player-includes file
  def upload2=(uploaded_io)
    unless self.name.blank?
      self.compressed_file_location = '' if self.compressed_file_location.nil?
      delete_code(self.compressed_file_location)
      self.compressed_file_location = store_file(uploaded_io, 'environments')[:file]
    end
  end

  # For referees - replay plugin file
  def upload3=(uploaded_io)
    unless self.name.blank?
      self.replay_assets_location = '' if self.replay_assets_location.nil?
      delete_code(self.replay_assets_location)
      self.replay_assets_location = store_file(uploaded_io, File.join("static", self.class.to_s.downcase.pluralize))[:directory]
    end
  end

  def file_location_exists
    if self.file_location.nil? || !File.exists?(self.file_location)
      errors.add(:file_location, "doesn't exist on the server")
    end
  end

  private

  def delete_code_locations
    delete_code(self.file_location)
    delete_code(self.compressed_file_location) if (self.has_attribute?(:compressed_file_location) && !self.compressed_file_location.nil?)
    delete_code(self.replay_assets_location) if (self.has_attribute?(:replay_assets_location) && !self.replay_assets_location.nil?)
  end

  # Delete directory where file is located
  def delete_code(location)
    pathname = Pathname.new(location)
    if not pathname.directory?
      location = pathname.dirname
    end
    FileUtils.rm_rf(location) if pathname.exist?
    if pathname.exist?
      raise "Deleting stuff it shouldnt"
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
    system("tar -xvf #{safe_src} -C #{safe_dest} > /dev/null 2>&1")
    system("unzip -o #{safe_src} -d #{safe_dest} > /dev/null 2>&1")
    mark_as_executable("#{safe_dest}/*")
    system("dos2unix -q #{safe_dest}/*")
  end

  def mark_as_executable(file)
    FileUtils.chmod('+x', file)
  end

  def random_hex
    SecureRandom.hex
  end
end

