validLinks = ['h:/hobo.ics.uci.edu/talk', 'h:hobo.ics.uci.edu/talk#123', 'h:hobo.ics.uci.edu/talk#dfasbnfmsdbfnmc']



defraggedLinks = [link.split('#', 1)[0] for link in validLinks]

print(defraggedLinks)
