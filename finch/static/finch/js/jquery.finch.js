(function($){
    $.fn.finch = function(options){
        // build main options before element iteration
        opts = $.extend({}, $.fn.contentmanager.defaults, options);
        return this.each(function(){
                if($('#smdialog').length===0){
                    var markup = '<div id="smdialog" title="Finch CMS"></div>';
                    $(document.body).append(markup);
                    $('#smdialog').dialog({
                            modal: true,
                                close: function(e, o){
                                close();
                            },
                                position: ['',30],
                                width: '80%',
                                resize: 'auto',
                                resizable: true, 
                                autoOpen: false
                                });
                    installHooks();
                }
            });
    };

    $.fn.finch.defaults = {};

    //
    // private function for debugging
    //
    function debug(msg) {
        if(window.console && window.console.log){
            window.console.log(msg);
        }
    };
    
    // This is called before the dialog is closed and will call any
    // callbacks that are passed via options
    function close(){
        debug('close called');
        if(opts.onclose){
            for(c in opts.onclose){
                opts.onclose[c]();
            }
        }
    };

    // This is called before a form (other than the listblocks-form)
    // is submitted
    function submit(){
        debug('submit called');
        if(opts.onsubmit){
            for(c in opts.onsubmit){
                opts.onsubmit[c]();
            }
        }
    }

    function getCallback(r){
        installHooks();
    };

    function installHooks(){
        $('#finch a.smlink').unbind('click').click(function(ev){
                $('#smdialog').load(ev.target.href, null, getCallback).dialog('open');
                return false;
            });
        $('#smdialog a.smlink').unbind('click').click(function(ev){
                $('#smdialog').load(ev.target.href, null, getCallback);
                return false;
            });
        $('#smdialog a.smcancel').unbind('click').click(function(ev){
                close();
                $('#smdialog').html('').dialog('close');
                return false;
            });
        $('#smdialog .smform').ajaxForm({
                complete: function(xhr, status){
                    if(xhr.responseText===''){
                        $('#smdialog').dialog('close');
                        if(xhr.getResponseHeader('X-Finch')){
                            window.location = xhr.getResponseHeader('X-Finch');
                        } else {
                            document.location.reload(true);
                        }
                    } else {
                        // Submit was unsuccesful
                        $('#smdialog').html(xhr.responseText).hide();
                        installHooks();
                        $('#smdialog').show();
                    }
                }
            });
    };
})(jQuery);
