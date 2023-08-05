(function() {



app.ready(function() {
   
})





app.data.networks = [
    {
        'id': '0x00',
        'label': '0x00 - app',
    },
    {
        'id': '0x01',
        'label': '0x01 - network nodefull',
    },
    {
        'id': '0x02',
        'label': '0x02 - network mixte'
    },
    {
        'id': 'dev',
        'label': 'local - dev',
        'checked': 'checked'
    },
    {
        'id': 'sandbox',
        'label': 'sandbox - ropsten'
    },
] 


// xio network nodeless
xio.handlers.bind('dev', function() {
    var network = xio.network({
        'server': 'http://127.0.0.1:8080',
        'ethereum': {
            'network': 'testrpc',
            'info': 'sdk/ext/inxio/contracts/inxio.dev.json',
        },
    })
    return network
})

// ropsten
xio.handlers.bind('sandbox', function() {
    var network = xio.network({
        'server': 'http://sandbox.inxio.net',
        'ethereum': {
            'network': 'ropsten',
            'info': 'sdk/ext/inxio/contracts/inxio.ropsten.json',
        },
       
    })
    return network

})






// no network => direct app
xio.handlers.bind('0x00', function() {
    return server
})

// xio network nodefull
xio.handlers.bind('0x01', function() {
    var network = xio.network({
        'server': server
    })
    return network
})

// xio network mixte
xio.handlers.bind('0x02', function() {
    var network = xio.network({
        'server': server,
        'ethereum': {
            'network': 'testrpc',
            'contract': 'latest',
        },
    })
    return network
})




})();
        
