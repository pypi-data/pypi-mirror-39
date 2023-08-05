
(function(){

    var LeafLetHandler = function(config) {

        this.config = config

        var id = this.config['id']
        var lat = this.config['latitude']
        var long = this.config['longitude']
        var zoom = this.config['zoom']
       
        this.map = L.map(id)
        this.map.setView([lat,long], zoom);

        this.addMarker = function(data) {

            //var marker = L.marker([51.505, -0.09]).addTo(this.map);
            //marker.bindPopup("I am a popup.").openPopup();  
            //return
            console.log('addmarket',data)

            var lat = data['latitude']
            var long = data['longitude']
            var info = data['description']
            var marker = L.marker([lat,long]).addTo(this.map);
            marker.bindPopup(info).openPopup();  
        }

        this.show = function() {
            var OpenStreetMap_Mapnik = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
	            maxZoom: 19,
	            attribution: 'OpenStreetMap'
            });
            OpenStreetMap_Mapnik.addTo(this.map);
        }
		return this

    }


	AppMap = function(id,config) {
        if (typeof id === 'string' || id instanceof String) {
		    console.log('create map from id #'+id)
            this.id = id;
            this.container = document.getElementById(this.id);
        } else {
            console.log('create map from element'+id)

            this.container = id;
            var id = $(this.container).attr('id')
            if (id) {
                this.id = id
            } else {
                this.id = 'uidmap123'; // tofix
                $(this.container).attr('id',id)
            }
        }
        console.log('map id='+this.id)
		
		this.config = config || {}
        this.handler = LeafLetHandler({
            'id': this.id,
            'zoom': this.config['zoom'] || 5,
            'latitude': this.config['latitude'] || 51.0,
            'longitude': this.config['longitude'] || 0    
        })
        this.show = function() {
		    //alert('show map',this)	
            this.handler.show(this.id);  
        }
        this.addMarker = function(data) {
            this.handler.addMarker(data);  
        }
		return this
	}
	AppMap.prototype = {
	}


})();

$(document).ready(function(){
	console.log('init lib geoloc')

    $.fn.xiomap = function(config) {
        var el = this[0]    
        if (config) {
            el._map = new AppMap(el,config)
        } else {
            if (!el._map) {
                el = this.closest('.map')[0]   
            }
        }
        console.log('map????',el._map)
        return el._map

    };

   
})


