import os
import sublime
import sys

st2 = (sys.version_info[0] == 2)
dist_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, dist_dir)

def plugin_loaded():
	from gosubl import about
	from gosubl import gs
	from gosubl import mg9

	gs.gs_init()
	mg9.gs_init()

	# we need the values in the file on-disk but we don't want any interference with the live env
	try:
		g = {}
		execfile(os.path.join(dist_dir, 'gosubl', 'about.py'), g)
		version = g.get('VERSION', '')
		ann = g.get('ANN', '')
		gs.set_attr('about.version', version)
		gs.set_attr('about.ann', ann)

		if about.VERSION != version:
			gs.show_output('GoSublime-source', '\n'.join([
				'GoSublime source has been updated.',
				'New version: `%s`, current version: `%s`' % (version, about.VERSION),
				'Please restart Sublime Text to complete the update.',
			]))
	except Exception:
		pass

	def cb():
		aso = gs.aso()
		old_version = aso.get('version', '')
		old_ann = aso.get('ann', '')
		if about.VERSION > old_version or about.ANN > old_ann:
			aso.set('version', about.VERSION)
			aso.set('ann', about.ANN)
			gs.save_aso()
			gs.focus(gs.dist_path('CHANGELOG.md'))

	sublime.set_timeout(cb, 0)


if st2:
	sublime.set_timeout(plugin_loaded, 0)
