module ApplicationHelper
    def setTitle(title)
        content_for(:title) { title }
    end
end
