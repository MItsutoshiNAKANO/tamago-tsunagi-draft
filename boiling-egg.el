; boiling-egg.el
; This file is Public Domain Software.
; Version 0.00  Apr  6, 2000  <sengoku@gcd.org>
; Version 0.01	Jul 31, 2000  <sengoku@gcd.org>
; Version 0.02	Oct 26, 2000  <sengoku@gcd.org>
;
; http://www.gcd.org/sengoku/boiling-egg/
;
; Define autoload entries and key bindings in your .emacs file as follows:
;
; (autoload 'boiling-rK-trans "boiling-egg" "romaji-kanji conversion" t)
; (autoload 'boiling-rhkR-trans "boiling-egg" "romaji-kana conversion" t)
; (global-set-key "\C-o" 'boiling-rK-trans)
; (global-set-key "\eo" 'boiling-rhkR-trans))

(defvar boiling-input-method "japanese-egg-wnn")
(defvar boiling-subjective-chars "[^]['.,a-zA-Z@-]")

(setq boiling-last-input-flag nil)

(defun boiling-rK-trans ()
  "(roman(hankaku) or hiragana/ktakana) -> KANJI transformation."
  (interactive)
  (if (boiling-rhkR-trans t)
      (progn
	(setq boiling-last-input-flag t)
	(activate-input-method boiling-input-method)
	(egg-convert-region boiling-trans-start (point)))))

(add-hook 'input-method-after-insert-chunk-hook
	  '(lambda ()
	     (if boiling-last-input-flag
		 (progn
		   (inactivate-input-method)
		   (setq boiling-last-input-flag nil)
		   (if (eq boiling-trans-start (point))
		       (insert-string boiling-trans-original))
		   ))
	     )
	  t)

(defun boiling-rhkR-trans (&optional kana)
  "roman(hankaku) -> hiragana -> katakana -> ROMAN(zenkaku) transformation"
  (interactive "P")
  (if (and (eq last-command 'boiling-rhkR-trans) boiling-trans-type)
      (cond
       (kana
	(delete-region boiling-trans-start (point))
	(insert-string boiling-trans-original)
	(boiling-rhR-trans boiling-trans-start (point) kana))
       ((eq boiling-trans-type 'h)
	(japanese-katakana-region boiling-trans-start (point))	  
	(setq boiling-trans-type 'k))
       ((eq boiling-trans-type 'k)
	(delete-region boiling-trans-start (point))
	(insert-string boiling-trans-original)
	(japanese-zenkaku-region boiling-trans-start (point))
	(setq boiling-trans-type 'R))
       ((eq boiling-trans-type 'R)
	(japanese-hankaku-region boiling-trans-start (point))
	(setq boiling-trans-type nil)
	t))
    (let ((pos (point))
	  (mark (mark t))
	  bol)
      (beginning-of-line)
      (setq bol (point))
      (goto-char pos)
      (if (and mark (<= bol mark) (< mark pos)
	       (not (re-search-backward "[^!-~]" mark t)))
	  (boiling-rhR-trans mark pos kana)
	(goto-char (- pos 1))
	(if (re-search-backward boiling-subjective-chars bol t)
	    (progn
	      (forward-char 1)
	      (boiling-rhR-trans (point) pos kana))
	  (boiling-rhR-trans bol pos kana))
	))
    ))

(defun boiling-rhR-trans (start end kana)
  (setq boiling-trans-start start)
  (goto-char end)
  (setq boiling-trans-original
	(buffer-substring boiling-trans-start end))
  (condition-case ()
      (progn
	(activate-input-method boiling-input-method)
	(inactivate-input-method)
	(its-translate-region boiling-trans-start (point))
	(setq boiling-trans-type 'h)
	t)
    (error
     (if kana
	 nil
       (goto-char end)
       (japanese-zenkaku-region boiling-trans-start end)
       (setq boiling-trans-type 'R)
       t)
     )))
