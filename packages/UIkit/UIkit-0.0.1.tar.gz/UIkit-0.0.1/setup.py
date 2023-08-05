from distutils.core import setup
setup(
  name = 'UIkit',         # How you named your package folder (MyLib)
  packages = ['UIkit'],   # Chose the same as "name"
  version = '0.0.1',      # Start with a small number and increase it with every change you make
  license='GNU LESSER GENERAL PUBLIC LICENSE v3',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Framework front-end para el desarrollo de aplicaciones con PyQt5',   # Give a short description about your library
  author = 'runesc_dev',                   # Type in your name
  author_email = 'fredogodofredodospuntosv@gmail.com',      # Type in your E-Mail
  url = 'https://github.com//runesc/Uikit/',   # Provide either the link to your github or to your website
  download_url = 'https://github.com//runesc/Uikit/',    # I explain this later on
  keywords = ['Front-end', 'PyQt5', 'Design'],   # Keywords that define your package best
  install_requires=[           
        'six',
        'PyQt5-sip',
        'PyQt5',
        'qtawesome'
      ]
)
