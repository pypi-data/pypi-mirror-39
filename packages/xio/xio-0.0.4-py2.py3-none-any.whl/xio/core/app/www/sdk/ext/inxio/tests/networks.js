

fakeapp = xio.app()
fakeapp.db = xio.db('fakeapp')
fakeapp.bind('', function(req) {
    alert('fake app')
    return {
        'method': req.method,
        'path': req.path,
        'query': req.query
    }
})

server = xio.app()
window.testserver = server // kesako ?
server.db = xio.db('test')
server.bind('*', function(req) {

    //console.log('TESTREQUEST FALLBACK',req)

    if (!req.path) {
        if (req.ABOUT)
            return {
                'name': 'fake network'
            }
    }

})
server.bind('store', function(req) {

    if (req.GET) {
        var filter = {'type': 'service'}
        return this.db.select(filter)
    }

})
server.bind('store/:id', function(req) {

    var id = req.context[':id']

    console.log('DB GET ID',id,req,this.db)
    var row = this.db.get(id)
    var type = row.type
    if (req.ABOUT) {
        return row
    }

    

    if (req.DELETE) {
        console.log('delete',id,req.data)
        this.db.delete(id)
        return 'ok'
    }    

    console.log('=========== MAKE REQUEST TO PROVIDER !!!!!!!!')
    return fakeapp.request(req)
    //return this.request(req.method,'handlers/'+id,req.data) // +'/'+req.path
})
server.bind('store/:id/offers', function(req) {

    var id = req.context[':id']
    var service = this.db.get(id)
    return service.offers
})
server.bind('store/:id/offers/:offerid', function(req) {

    var id = req.context[':id']
    var offerid = req.context[':offerid']
    
    var service = this.db.get(id)
    var offer = null
    $(service.offers).each(function(){
        if (this.id==offerid)
            offer = this
    })
    
    console.log('FAKE PURCHASE',service,offer)
    if (req.ABOUT) {
        return offer
    }
    if (req.PURCHASE) {
        var newid = Date.now().toString();
        var order = {
            'id': newid,
            'type': 'order',
            'owner': xio.context.user.id,
            'seller': service.owner,
            'buyer': xio.context.user.id,
            'item': service.id,
            'offer': offerid,
            'input': req.data.input,
            'status': 'done'
        }

        server.db.put(newid,order)
        server.db.patch(id,{'ttl': Date.now()+3600})
        return newid
    }
})

server.bind('store/:id/orders', function(req) {
    var id = req.context[':id']
    return this.db.select({
        'type':'order',
        'owner': xio.context.user.id,
        'item': id
    })
})
server.bind('store/:id/instances', function(req) {
    var id = req.context[':id']
    if (req.GET) {
        return this.db.select({
            'type':'resource',
            'owner': xio.context.user.id,
            'handler': id
        })
    }
    if (req.CREATE) {
        console.log('create',id,req.data)
        var newid = Date.now().toString();
        var data = {
            'id': newid,
            'type': 'resource',
            'owner': xio.context.user.id,
            'handler': id,
            'input': req.data
        }
        server.db.put(newid,data)
        return newid
    }

    if (req.CONFIGURE) {
        console.log('configure',id,req.data)
        this.db.patch(id,{'input':req.data})
        return 'ok'
    }

})

server.bind('user', function(req) {
    return this.db.get(xio.context.user.id)
})

server.bind('user/services', function(req) {
    return this.db.select({
        'type':'service',
        'owner': xio.context.user.id
    })
})
server.bind('user/sales', function(req) {
    return this.db.select({
        'type':'order',
        'seller': xio.context.user.id
    })
})
server.bind('user/purchases', function(req) {
    return this.db.select({
        'type':'order',
        'buyer': xio.context.user.id
    })
})
server.bind('user/store', function(req) {
    var self = this
    var d = $.Deferred()
    console.log('*****FAKE START')
    setTimeout(function(){
        var result = self.db.select(function(row) {
            return (row.type=='service' && row.offers)
                //return (row.type=='service' && row.offers)
        })
        console.log('*****FAKE STOP')
        //alert('*****FAKE STOP')
        d.resolve(result)
    }, 100);

    return d.promise() 
})


server.bind('handlers/01', function(req) {

    return 'store01 service response for '+req.method+' '+req.path

})
server.handleResource = function(req) {

}

/*
server.bind('services', function(req) {
    if (req.ABOUT)
        return {
            'name': 'services'
        }
    if (req.GET)
        return this.db.select({'type':'service'})
})
server.bind('tasks', function(req) {
    if (req.ABOUT)
        return {
            'name': 'tasks'
        }
    if (req.GET)
        return this.db.select({
            'type':'tasks',
            'handler': xio.context.user.id
        })
})

server.bind(':id', function(req) {
    var peerid = req.context[':id']
    if (req.ABOUT) {
        return this.db.get(peerid)
    }
    if (req.DOSOMETHING) {
        return 'i did something for '+peerid
    }
    if (req.PURCHASE || req.SUBSCRIBE) {
        var newid = Date.now().toString();
        var about = {
            'id': newid,
            'owner': xio.context.user.id,
            'name': req.data.name,
            'handler': peerid,
            'input': req.data.input
        }
        about = xio.tools.about(about)
        server.db.put(id,about)
    }
    if (req.UPDATETASK) {
        var data = this.db.get(peerid)
        data['output'] = req.data.output
        data['status'] = req.data.status
        //alert(JSON.stringify(req.data))
        server.db.put(peerid,data)
        alert('?? '+JSON.stringify(req.data))
    }
})
*/




$.getJSON( 'tests/network.data.json').then( function( data ) {

    $(data).each(function(){
        var path = '/'+this.name
        var about = xio.tools.about(this)
        var id = this.id || this.name
        server.db.put(id,this)
    })
})












