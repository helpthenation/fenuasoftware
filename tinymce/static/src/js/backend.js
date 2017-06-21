odoo.define('tinymce.backend', function(require) {
	"use strict";

	var core = require('web.core');
	var session = require('web.session');
	var Model = require('web.DataModel');
	var common = require('web.form_common');
	var base = require('web_editor.base');
	var editor = require('web_editor.editor');
	var summernote = require('web_editor.summernote');
	var transcoder = require('web_editor.transcoder');
	var backend = require('web_editor.backend');

	var QWeb = core.qweb;

	var FieldTextTinyMCESimple = common.AbstractField.extend(common.ReinitializeFieldMixin, {
		template : 'tinymce.FieldTextTinyMCESimple',

		init : function(field_manager, node) {
			this._super(field_manager, node);
		},

		initialize_content : function() {
			if (!this.get('effective_readonly') && !this.$input) {
				this.$textarea = this.$('textarea');
			}
			this.setupFocus(this.$el);
		},

		destroy_content : function() {
			if (this.$textarea) {
				this.$textarea.destroy();
				this.$textarea = undefined;
			}
		},

		render_value : function() {
			var show_value = this.get('value');
			if (this.$textarea) {
				this.$textarea.val(show_value);
				this.$textarea.tinymce({
					theme : 'modern',
					toolbar1 : 'undo redo | insert | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent | link image',
					toolbar2 : 'print preview media | forecolor backcolor emoticons | codesample help',
					plugins : [ 'advlist autolink lists link image charmap print preview hr anchor pagebreak', 'searchreplace wordcount visualblocks visualchars code fullscreen', 'insertdatetime media nonbreaking save table contextmenu directionality', 'emoticons template paste textcolor colorpicker textpattern imagetools codesample toc help' ],
					image_advtab : true,
				});
			} else {
				this.$el.html(this.text_to_html(show_value));
			}
		},

		commit_value : function() {
			if (this.$textarea) {
				this.internal_set_value(this.$textarea.val());
			}
			return this._super();
		},

		text_to_html : function(text) {
			var value = text || "";
			try {
				$(text)[0].innerHTML;
				return text;
			} catch (e) {
				if (value.match(/^\s*$/)) {
					value = '<p><br/></p>';
				} else {
					value = "<p>" + value.split(/<br\/?>/).join("<br/></p><p>") + "</p>";
					value = value.replace(/<p><\/p>/g, '').replace('<p><p>', '<p>').replace('<p><p ', '<p ').replace('</p></p>', '</p>');
				}
			}
			return value;
		},
	});

	core.form_widget_registry.add('tinymce', FieldTextTinyMCESimple);

	return {
		FieldTextTinyMCESimple : FieldTextTinyMCESimple,
	};

});