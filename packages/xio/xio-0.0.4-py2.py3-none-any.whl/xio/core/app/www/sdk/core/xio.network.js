(function(){


    class XioNetwork extends XioResource {

        constructor(config) {
            super();  
            this.config = config
            if (config.ethereum) {
                var handler = new XioNetworkEthereumHandler(config)
                this.handler = xio.client(handler)
            } else if (config.server) {
                var handler = config.server
                this.handler = handler //xio.client(handler) 
            }
        }

        request(method,path,data,headers,context) {
            var self = this
            if (!(method instanceof XioRequest)) {
                var req = xio.request(method,path,data,headers,context)
            } else {
                var req = method
            }
            return this.handler.request(req)
        }
    }

    window.XioNetwork = XioNetwork

})();

