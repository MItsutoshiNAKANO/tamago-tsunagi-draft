(load "/usr/share/emacs/site-lisp/egg/leim-list")

;; egg-canna.el makes the CANNA commands of emcws available with tamago. 
;; egg-canna.el is already part of the tamago package in SuSE GNU/Linux.
;; to use it you need the following hook:

(add-hook 'canna-load-hook '(lambda () (load "egg-canna.el")))

