
(function(){

	function _sort(iso,key) {
		return function(el) {
			return iso.sortHandler(key,el)
		}
	}

	AppIsotope = function(id,config) {
        var self = this
        if (typeof id === 'string' || id instanceof String) {
            this.id = id;
            this.container = document.getElementById(this.id);
        } else {
            this.container = id;
        }

		this.data = {}
		this.config = config || {}
        if (!this.config['itemSelector'])
		    this.config['itemSelector'] = '.item'

        if (this.config['itemTemplate'])
            this.template = this.config['itemTemplate']

		//this.config['masonry'] =  {columnWidth: '.item-sizer'}

        if (this.config['data']) {
		    // dyn sort data

		    var datasort = this.config['data']['sort'];
		    this.config['getSortData'] = {};
		    for (i in datasort) {
			    var key = datasort[i];
			    this.config['getSortData'][key] = _sort(this,key)
		    }
		    //this.config['getSortData'] = getSortData;
        }

		/*
		getSortData:{
			title: '[data-title]',
			rating: function( e ) { 
			  return parseInt( $(e).data('rating') );
			},
		}
		*/
		this.current_xhr = null
		this.iso = new Isotope( this.container, this.config)
        this.parentIso = $(this.container).parent().closest('.isotope').iso()
        this._events = {}
        if (!this.template) {
		    this.template = $(this.container).find('.iso-default-template').html()
		    $(this.container).find('.iso-default-template').remove()
        } 

        this.iso.on('arrangeComplete', function() {
            self.propagate()
        })
        this.iso.on('layoutComplete', function() {
            self.propagate()
        })
		return this
	}
	AppIsotope.prototype = {

        on: function(event,callback) {
            this._events[event] = callback
        },
        fire: function(event,data) {
            data = data || null
            if (this._events[event]) 
                this._events[event](data)        
        },

        setView: function(view) {
            $(this.container).removeClass('view view-rows view-grid')
            $(this.container).addClass('view view-'+view)
            this.refresh()
        },

		sortHandler: function(key,el) {

			var id = $(el).data('id')	
			//var value =  parseInt( this.data[id][key] )
			if (this.data[id]) {
				var value =  this.data[id][key] 

			}
			return value;	
		},

		fill: function(data) {
			
			var template = this.template[0]
			var html = Mustache.to_html(this.template,data);

			$(this.container).html(html);
			this.iso = new iso(this.container, this.config);
		},

		push: function(data) {
            var self = this
            console.log('iso push')

            // cas d'un jquery 
            if (data instanceof jQuery) {
                if (!data.hasClass('item'))
                    data.addClass('item')
                this.iso.insert( data ) 
                return data
            }

            // cas d'un string html
            if (typeof data === 'string' || data instanceof String) {
                var html = data
                var els = $.parseHTML(html.trim())
                $(els).each(function(){
                    if (!$(this).hasClass('item'))
                        $(this).addClass('item')
                })
                this.iso.insert( els ) 
                return els
            }


			var template = this.template
			for(var i in data) {
				
   				var html = Mustache.to_html(template,data[i]);
				var els = $.parseHTML(html.trim())
				for (j in els) {
					var id = $(els[j]).data('id')
					
					if (!id) {
						var id = Object.keys(this.data).length
						$(els[j]).data('id', id)
					}
					this.data[id] = data[i]
				}
				
				this.iso.insert( els ) 
			}
			return els
		},

		filter: function(key,val) {
            var self = this
            var d = $.Deferred();

            if (typeof val === "function") {
                callback = val;
                val = undefined;
            }

			this.iso.once( 'layoutComplete', function() {
                d.resolve(true)
            })
			
			
            if (val!=undefined) {
			    this.iso.arrange({ filter: function() {
				    return (val==$(this).data(key))
			    }});
            } else {
			    this.iso.arrange({ filter: key});
            }
            return d.promise()
		},

        hide: function($items) {
            var els = [];
            var self = this
            $items.each(function() {
                els.push( self.iso.getItem($(this)[0]) );
                //self.iso.hide( self.iso.getItem($(this)[0]) )
            });  
            this.iso.hide( els )

        },

        remove: function(target) {
            if (typeof target === 'string' || target instanceof String) {
                target = $(this.container).find(target) 
            }
            this.iso.remove( target)   
			this.iso.layout();	 
        },

		sort: function(key,asc) {
			if (asc==null) asc = true 
			this.iso.arrange({
				sortBy:key,
				sortAscending: asc
			})
		},

		refresh: function(callback) {
            var self = this
            //console.log('iso refresh ')

            this.iso.once( 'layoutComplete', function() {
                if (callback) {
                    callback()
                }
            })

			this.iso.layout();
		},

        propagate: function() {
            if (this.parentIso) {
                console.log('iso propagate to ',this.parentIso)
                this.parentIso.refresh()
            }
        },


		clear: function(callback) {
			this.iso.remove( $('.item:not(.isoheader)') )
			if (callback) {
				this.iso.once( 'layoutComplete', callback )
			}
			this.filter() // clear previous filter
			this.iso.layout();	
			this.start = null
		},

		
		load: function(extraparams,callback) {
			this.iso.remove( $( this.container ).find('.loader') )
			if(typeof extraparams == "function") {
				callback = extraparams
				extraparams = {}
			}

			var params = params || {}
			var datasource = this.config['data']['datasource']
			var params = this.config['data']['params'] || {}
			for (key in extraparams) {
				params[key] = extraparams[key]
			}
			var limit = this.config['data']['limit']
			if (this.start == null) {
				this.start = 0	
			} else {	
				this.start += 1
			}
			params['limit'] = limit
			params['start'] = this.start*limit

			if (this.current_xhr) {
				this.current_xhr.abort();
			}

			var iso = this
			this.current_xhr = app.get(datasource,params,function(data) {
				iso.current_xhr = null
				iso.push( data )	
				if (data.length==limit) { 
					iso.datanext = true
					var elem = $('<div class="item loader"></div>').click(function(){ 
						
						iso.load() 
					})
					$( iso.container ).append( elem )
					iso.iso.appended( elem ) 	// $("<div></div>");
				} else {
					iso.datanext = false
				}

				iso.iso.updateSortData( iso.config['itemSelector'] )
				if (callback) {
					callback()
				}
			})
		},


        selectItem: function(item) {
            var self = this
            item.addClass('selected')
            this.filter('.selected').then( function() {
                self.fire('select',item)
            }) 
        },


        unSelectItem: function(item) {
            var self = this
            item.removeClass('selected')
            this.filter().then( function() {
                self.fire('unselect',item)
            }) 
        },

        

        enhance: function() {


            //$(this.container).enhance() // app enhance ?

            var target = $(this.container)
            var self = this


            $(target).find('.cover').unbind('click').bind('click', function(event) { 
                var item = $(this).closest('.item')
                if (item.hasClass('selected')) {
                    self.unSelectItem(item)    
                } else {
                    self.selectItem(item)  
                }
            })

            $(target).find('*[data-iso-select]').unbind('click').bind('click', function(event) { 

                // check a@href
                var href = $(event.target).attr('href')
                if (!href) {
                

                    if ( $(this).hasClass('item') ) {
                        var item = $(this)
                    } else {
                        var item = $(this).closest('.item') 
                    }
                    var selected = $(item).hasClass('selected') 
                    var callbackname = $(this).data('iso-select')
                    var callback = window[callbackname]

                    if (selected) {
                        $(item).removeClass('selected') 
                        $(item).iso().filter()
                        callback(item,false)
                    } else {
                        $(item).addClass('selected').siblings().removeClass('selected') 
                        $(item).iso().filter('.selected')
                        callback(item,true)
                    }
                    return false;
                }
            }),


            $(target).find('*[data-iso-view]').unbind('click').bind('click', function() { 

                var container = $(this).closest('ul')
                var currentview = container.find('.active').data('iso-view') 
                var newview = $(this).data('iso-view')
                container.find('.active').removeClass('active')
                $(this).addClass('active')

                var target = $(this).closest('*[data-iso-target]').data('iso-target')
                if (!target) {
                    var target = $(this).closest('.iso')  
                }
                $(target).removeClass('view1 view2 view3 view3 view4 view5').addClass(newview)
                $(target).iso().refresh()
                return false;
            })

            $(target).find('*[data-iso-filter]').unbind('click').bind('click', function() {
                var cls = $(this).data('iso-filter') 
                var target = $(this).closest('.iso')
                if (!target.length) {
                    var target = $(this).closest('*[data-iso-target]').data('iso-target')
                }
                $(target).iso().filter(cls)
                return false;
            })

        },

	}


})();


$.fn.iso = function(config) {
    var el = this[0]    
    if (!el)
        return null
    if (config) {
        el._iso = new AppIsotope(el,config)
    } else {
        if (!el._iso) {
            el = this.closest('.isotope')[0]   

        }
    }
    if (el)
        return el._iso 
    else 
        return null
};

   




