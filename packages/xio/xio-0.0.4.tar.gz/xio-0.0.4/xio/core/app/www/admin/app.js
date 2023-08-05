

app.ready( function() {
    var endpoint = app.nav.context.endpoint || document.location.href
    app.about.name = endpoint
    return app.user.connect(endpoint).then(function(client) {
        app.server = client
        return app.server.about().then(function(resp) {
            return resp.content
        })
    })
})

app.enhance(function() {
    $(this).find('*[data-xio-nav]').click(function(el){
        var href = $(this).data('xio-nav')
        app.render(href)
    })
})
