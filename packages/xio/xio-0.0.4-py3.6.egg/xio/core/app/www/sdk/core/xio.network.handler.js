(function(){

    function toBytes(str) {
        return web3.fromAscii(str)
    }

    function fromBytes(value) {
        value = value || ''
        return web3.toAscii(value).replace(/\u0000/g, '')
    }

    function cleanAddresses(addresses) {
        var cleaned = []
        addresses.forEach(function(address) {
            if (!address.startsWith('0x0000'))
                cleaned.push(address)
        });
        return cleaned;
    }

    BASE_ABI = [
        {
            "constant": true,
            "inputs": [],
            "name": "about",
            "outputs": [
                {
                    "name": "",
                    "type": "string"
                }
            ],
            "payable": false,
            "stateMutability": "view",
            "type": "function"
        }
    ]



    class XioNetworkEthereumHandler extends XioResource {

        constructor(config) {
            super();  
            var self = this

            this.STATUS_NEW = 0
            this.STATUS_ACTIVE = 1
            this.STATUS_RUNNING = 2
            this.STATUS_PENDING = 3
            this.STATUS_COMPLETED = 9   
            this.PRICING_TYPE_SUBSCRIPTION = 1
            this.PRICING_TYPE_PURCHASE = 2
            this.RESOURCE_TYPE_RESOURCE = 0
            this.RESOURCE_TYPE_NETWORK = 1
            this.RESOURCE_TYPE_USER = 2
            this.RESOURCE_TYPE_SERVICE = 3
            this.RESOURCE_TYPE_OFFER = 4
            this.RESOURCE_TYPE_ORDER = 5
            this.RESOURCE_TYPE_ORDERITEM = 6
            this.RESOURCE_TYPE_SUBSCRIPTION = 6
            this.TYPE_MAPPING_BY_NAME = {
                'resource': 0,
                'network': 1,
                'user': 2,
                'service': 3,
                'offer': 4,
                'order': 5,
                'orderitem': 6,
                'subscription': 7
            }
            this.TYPE_MAPPING_BY_CODE = {
                0: 'resource',
                1: 'network',
                2: 'user',
                3: 'service',
                4: 'offer',
                5: 'order',
                6: 'orderitem',
                7: 'subscription'
            }

            this.config = config
            this.uri = config.id
            this._about = {}
            this._sync = {
                'block': 0,
                'updated': 0
            }


            var dbname = xio.tools.md5( 'inxio-network-'+this.uri )
            this.db = xio.db(dbname)
            //this.db.truncate() ////////////////////////////////////// debug


            if (config.server) {
                this.server = xio.client(config.server)
                this.server._token = xio.context.user.token
            } else {
                this.server = null
            }


            if (typeof Ipfs === 'function') {
                this.ipfs = new Ipfs()
            } 
            if (typeof Ethereum === 'function') {
                this.ethereum = new Ethereum({network:config.ethereum.network})
            }


            // set handlers

            app.on('logout', function() {
                alert('remove db')
                self.db.truncate()
            })
            app.on('login', function() {
                alert('remove db')
                self.db.truncate()
            })

            // set routes

            this.bind('services', function(req) { 
                // proxy
                if (req.GET) {
                    return this.getResources('service', function(row) {
                        if (row.type=='service') {
                            if (row.owner == req.client.id) 
                                return true
                            if (row.subscription)
                                return true
                        }
                    })
                }
                return self.server.request(req) 
            }) 
            this.bind('services/:id', this.handleService)
            this.bind('services/:id/*', this.handleService)
            this.bind('store', function(req) {
                if (req.GET) {
                    return this.getResources('service',{'type':'service'})
                }
            })
            this.bind('store/:id', this.handleStoreItem)
            this.bind('store/:id/offers', function(req) {

                if (req.ABOUT)
                    return {
                        'options': ['GET']
                    }

                var serviceid = req.context[':id']
                return self.getResource(serviceid).then(function(service) {
                    return service.offers
                })
                
                /*
                var filter = {'type': 'offer','item': serviceid}
                return this.contract.getOffers(serviceid).then(function(ids) {
                    var dl = []
                    $(ids).each(function (i,id) {
                        var d = self.getResource(id,'offer').then(function(data) {
                            //console.log(data)
                        })
                        dl.push( d )
                    })

                    return $.when.apply($,dl).then(function () {
                        return self.db.select(filter)
                    }, function(err) {
                        alert(err)
                    })

                })
                */
            })
            this.bind('store/:id/offers/:offerid', function(req) {

                var serviceid = req.context[':id']
                var offerid = req.context[':offerid']

                var service = self.getResource(serviceid)
                
                if (req.ABOUT) {
                    return self.aboutResource(offerid,'offer').then(function(about) {
                        about.options.push('PURCHASE')
                        return about
                    })
                }

                if (req.PURCHASE) {

                    var offer = this.db.get(offerid)
                    var input = '0x' //req.data
                    var about = ''

                    var cost = offer.cost
                    var value = new XioValue('amount',cost,'EUR')
                    // fix pb converstion rate

                    return self.contract.eur2wei(cost).then(function(value_wei) {
                        var dialog = {
                            'title': 'transaction '+cost+' EUR',
                            'content': 'Do youy confirm payment of '+value_wei+' WEI'
                        }
                        return app.ui.confirm(dialog).then(function() {

                            var context = {
                                'value': value_wei
                            }
                            return self.contract.purchase(serviceid, offerid, 1, input, context)
                        })
                    })

                }
            })
            this.bind('store/:id/purchases', function(req) {
                var serviceid = req.context[':id']
                var filter = {'type': 'order', 'item': serviceid}
                return this.getResources('order',filter)
            })
            this.bind('store/:id/purchases/:orderid', function(req) {
                var orderid = req.context[':orderid']
                return self.getResource(orderid)
            })
            this.bind('store/:id/orders', function(req) {
                if (req.GET) {
                    var serviceid = req.context[':id']
                    var filter = {'type': 'order', 'item': serviceid}
                    return this.getResources('order',filter)
                }
            })
            this.bind('store/:id/orders/:orderid', function(req) {
                var orderid = req.context[':orderid']
                return self.getResource(orderid)
            })

            this.bind('user', function(req) {
                return this.handleUser(req)
            })
            this.bind('user/purchases', function(req) {
                if (req.ABOUT) {
                    return {'options': ['GET']} 
                }
                if (req.GET) {
                    var filter = {'type': 'order', 'buyer': req.client.id}
                    return this.getResources('order',filter)
                }
            })
            this.bind('user/purchases/:orderid', function(req) {
                var orderid = req.context[':orderid']
                return self.getResource(orderid)
            })
            this.bind('user/sales', function(req) {
                if (req.ABOUT) {
                    return {'options': ['GET']} 
                }
                if (req.GET) {
                    var filter = {'type': 'order', 'seller': req.client.id}
                    return this.getResources('order',filter)
                }
            })
            this.bind('user/sales/:orderid', function(req) {
                var orderid = req.context[':orderid']
                return self.getResource(orderid)
            })
            this.bind('user/subscriptions', function(req) {
                if (req.ABOUT) {
                    return {'options': ['GET']} 
                }
                if (req.GET) {
                    return this.getResources('service', function(row) {
                        if (row.subscription)
                            return true
                    })
                }
            })
            /*


            this.bind('store/:id/instances', function(req) {
                var serviceid = req.context[':id']
                if (req.GET) {
                    var filter = {'type': 'resource', 'handler': serviceid}
                    return this.getResources('resource',filter)
                }
                if (req.CREATE) {
                    var input = req.data
                    var d1 = this.ipfs.put(input)
                    return $.when( d1 ).done(function ( input ) {
                        var name = toBytes('noname')
                        var about = toBytes('')
                        var input = toBytes(input)
                        var output = toBytes('')
                        return self.contract.createUserResource(name,about,serviceid,input,output)
                    })
                }

            })
           */
        }

        sync() {
            var self = this
            console.log('sync')
            var block = this._sync.block
            this.contract.events.get('logResourceUpdated',{fromBlock: block, toBlock: 'latest'}).then(function(rows) {
                console.log(rows)
                // returnValues
                var dl = []
                $(rows).each(function() {
                    var eventblock = this.blockNumber
                    var eventdata = this.returnValues
                    var id = eventdata[0]
                    console.log( '...resync', id )
                    dl.push( 
                        self.loadResource(id).then(function() {
                            if (eventblock>self._sync.block) {
                                self._sync.block = eventblock
                            }
                        }) 
                    )
                })
            })
        }

        connect() {
            
            var self = this
            var config = this.config
            var contract = config.ethereum.contract
            var abi = config.ethereum.abi
            var address = config.ethereum.address
            var info = config.ethereum.info
            if (abi && address) {
                var d = {
                    'address': address,
                    'abi': abi,
                }
            } else if (info) {
                var d = $.getJSON(info)
            } 
            return $.when(d).then( function( data ) {
                self.address = data.address
                self.abi = data.abi
                self.contract = self.ethereum.contract(self.abi,self.address,'Inxio')
                return self.contract.about()
            }).then(function(aboutcontract) {
                var habout = fromBytes( aboutcontract[6] )
                return self.ipfs.get(habout)
            }).then(function(about){
                console.log(about)
                self._about = about
                if (about.snapshot) {
                    self._sync.updated = about.snapshot.created
                    self._sync.block = about.snapshot.block
                    self._sync.service = true
                    $(about.snapshot.resources).each( function() {
                        var service = this
                        console.log('.. load from snapshot',service)
                        var userid = xio.context.user.id
                        self.db.put(service.id,this)
                        self.getUserSubscription(userid,service.id).then(function(subscription) {
                            if (subscription.ttl) {
                                service.subscription = subscription
                                self.db.patch(service.id,{
                                    'subscription': subscription
                                })
                            }
                        })
                    })
                }
                console.log('network ready')
            })
        }

        render(req) {
            var self = this
            /*
            if (!(method instanceof XioRequest)) {
                var req = xio.request(method,path,data,headers,context)
            } else {
                var req = method
            }
            */

            console.log('XioNetworkEthereumHandler>>> RENDER',req)
            
            if (!req.path) {
                return this.handleNetwork(req)
            }
            return this.request(req)
            /*
            var info = this._routes.getHandler(p)

            if (!info) {
                alert('no routes for '+req.path)
                return 
            }

            var handler = info.handler
            var postpath = info.postpath
            var context = info.context
            var req = xio.request(req.method,postpath,req.data,{},context)
            var result = handler.call(this, req)
            
            return $.when(result).then(function(result) {
                return result
            })
            */
        }

        aboutResource(id) {
            var self = this
            return this.getResource(id).then(function(row) {
                return self.resolve(row)
            }).then(function(row) {
                return xio.tools.about( row )
            })
        }

        resolve(row) {

            if (!row)
                return $.Deferred().resolve(row).promise()

            console.log('====== ABOUT RESOLVE BEFORE',row)
            var self = this

            var ipfs_keys = ['about','input','output'] //,'input','output']
            var link_keys = [] //'handler','item'] //['owner','seller','buyer','worker','item','offer','handler']

            var dl = []

            for (var k in row) {
                var v = row[k]
                //console.log('RESOLVE',k,v)
                var resolve = null
                if (ipfs_keys.indexOf(k)!=-1) {
                    resolve = function(key,value) {
                        return self.ipfs.get(value).then(function(result){
                            //xio.log.debug('====== ... RESOLVE IPFS',key,value,result)
                            row[key] = result || ''
                        })
                    }
                } else if (link_keys.indexOf(k)!=-1 && v!='0') {
                    resolve = function(key,value) {
                        return self.get(value).then(function(result){
                            //xio.log.debug('====== ... RESOLVE LINK',key,value,result)
                            row[key] = result || {'id':value}
                        })
                    }
                }
                if (resolve && (typeof v === 'string' || v instanceof String)) {
                    dl.push( resolve(k,v) )
                }

            }
            
            //console.log('DL>>>',dl)
            return $.when.apply($,dl).then(function () {
                console.log('====== ABOUT RESOLVE AFTER',row)
                return row
            })
        }


        getUserSubscription(userid, serviceid) {
            return this.contract.getUserSubscription(userid,serviceid).then(function(result) {
                return {
                    'profile': fromBytes(result[0]),
                    'ttl': parseInt(result[1]), // bug uint ?
                }
            })
        }

        getResources(type,filter) {
            var self = this
            filter = filter || {}
            filter['type'] = type

            var d = $.Deferred()
            if (!this._sync[type]) {
                this._sync[type] = true
                d = self.loadResources(type)
            } else {
                d = true
            }
            return $.when(d).then( function() {
                return self.db.select(filter)
            }) 
        }
        getResource(id,refresh) {
            var self = this
            var d = $.Deferred()
            var cached = this.db.get(id)
            if (cached && !refresh) {
                return d.resolve(cached).promise();
            }
            return this.loadResource(id)
        }
        loadResources(type) {
            var self = this
            var typecode = this.TYPE_MAPPING_BY_NAME[type];
            console.log('loadResources ...',type)
            return this.contract.getResources(typecode,0).then(function(ids) {
                var dl = []
                $(ids).each(function (i,id) {
                    if (id && ! id.startsWith('0x00000')) {
                        var d = self.loadResource(id)
                        dl.push( d )
                    }
                })
                return $.when.apply($,dl)
            })
        }
        loadResource(id) {
            var self = this
            console.log('loadResource ...',id)
            var d = $.Deferred()
            
            // quick & dirty

            if (!id || id=='0' || String(id).startsWith('0x000'))  {
                return d.resolve(null).promise();
            }

            // 
            
            return self.contract.aboutResource(id).then(function(data) {

                var typecode = data[0];
                var id = data[1];
                var owner = data[2];
                var name = data[3];
                var about = data[4];
                var status = data[5];
                var result = {
                    'id': id,
                    'type': self.TYPE_MAPPING_BY_CODE[typecode],
                    'owner': owner,
                    'status': status,
                    'name': fromBytes(name),
                    'about': fromBytes(about),
                }
                console.log(result)
                
                return result
            }).then(function(data) {
                return self.ipfs.get(data['about']).then(function(about) {
                    data['_about'] = data['about']
                    data['about'] = about
                    return data
                })
            }).then(function(data) {

                    var type = data['type']

                    if (type=='user') {

                        return self.contract.aboutUser(id).getContent().then(function(extra) {
                            data['level'] = extra[0]
                            data['credit'] = extra[1]
                            return data
                        })
                    }
                    else if (type=='resource') {
                        return self.contract.aboutUserResource(id).then(function(extra) {
                            data['_debug'] = extra
                            data['handler'] = extra[0]
                            data['input'] = extra[1]
                            data['output'] = extra[2]
                            return data
                        })
                    }
                    else if (type=='order') {
                        /*
                        order.buyer,
                        order.orderItem.seller,
                        order.orderItem.item,
                        order.orderItem.quantity,
                        order.orderItem.input,
                        order.orderItem.provider,
                        order.orderItem.output,
                        order.orderItem.delivered
                        */
                        return self.contract.aboutOrder(id).then(function(extra) {
                            data['_debug'] = extra
                            data['buyer'] = extra[0]
                            data['seller'] = extra[1]
                            data['item'] = extra[2]
                            data['quantity'] = extra[3]
                            data['input'] = extra[4]
                            data['provider'] = extra[5]
                            data['output'] = extra[6]
                            data['delivered'] = extra[7]
                            return data
                        })
                    }
                    else if (type=='offer') {
                        return self.contract.aboutOffer(id).then(function(extra) {
                            data['_debug'] = extra
                            data['seller'] = extra[0]
                            data['item'] = extra[1]
                            data['pricing'] = extra[2]
                            data['cost'] = extra[3]
                            data['profile'] = extra[4]
                            data['ttl'] = extra[5]
                            return data
                        })
                    }                
                    else if (type=='orderitem') {
                        return self.contract.aboutOrderItem(id).then(function(extra) {
                            data['_debug'] = extra
                            data['order'] = extra[0]
                            data['item'] = extra[1]
                            data['offer'] = extra[2]
                            data['provider'] = extra[3]
                            data['input'] = extra[4]
                            data['output'] = extra[5]
                            data['quantity'] = extra[6]
                            data['shipped'] = extra[7]
                            return data
                        })
                    }
                    else if (type=='service') {
                        return self.contract.aboutService(id).then(function(extra) {
                            data['_debug'] = extra
                            data['input'] = extra[0]
                            data['output'] = extra[1]
                            data['seller'] = extra[2]
                            data['provider'] = extra[3]
                            data['offers'] = extra[4]
                            return data
                        }).then(function() {
                            // load subscription - some contract method missing
                            // all user specific must go to dedicated db ?
                            var userid = xio.context.user.id
                            return self.contract.getUserSubscription(userid, data['id']).then(function(extra) {
                                data['subscription'] = {
                                    'profile': extra[0],
                                    'ttl': extra[1],
                                    'max_request': extra[2],
                                    'max_storage': extra[3],
                                    'max_items': extra[4],
                                }
                                data['subscribed'] = data['subscription']['ttl']>0
                                return data
                            })
                        })
                    }
                    return data


            }).then(function(data) {
                console.log('****** PUT DB', id, data)
                self.db.put(id,data) 
                return data
            })

        }

        handleNetwork(req) {
            var self = this

            if (req.CONNECT) {
                return $.when( self.connect() )
            }

            if (req.ABOUT) {

                var d1 = this.contract.about().then( function (data) {

                    var network = data[0];
                    var id = data[1];
                    var owner = data[2];
                    var typecode = data[3];
                    var status = data[4];
                    var name = data[5];
                    var about = data[6];

                    var result = {
                        'network': network,
                        'id': id,
                        'type': self.TYPE_MAPPING_BY_CODE[typecode],
                        'owner': owner,
                        'status': status,
                        'name': name,
                        'about': about,
                        'fee': data[7],
                        'rate': data[8],
                        'rate_updated': data[9],
                        'sync': self._sync
                    }

                    return self.ipfs.get(about).then(function (about) {
                        result.about = about
                        return result
                    })
                })
                return $.when( d1 )

            }



        }


        handleService(req) {

            var self = this

            console.log(req)

            var id = req.context[':id']

            var row = this.db.get(id)
            var type = row.type

            if (req.ABOUT) {
                return self.aboutResource(id)
            }

            alert('to upstream '+req.method+' '+req.path)
            console.log('unhandled request ... forward to upstream', req)
            req.path = xio.tools.path(id,req.path)
            return self.server.request(req)

        }

        handleStoreItem(req) {

            var self = this

            console.log(req)

            var id = req.context[':id']

            var row = this.db.get(id)

            if (!row) {
                req.path = id+'/'+req.path
                return self.server.request(req)
            }

            var type = row.type

            if (req.ABOUT) {
                return self.aboutResource(id).then(function(about) {
                
                    if (about.type=='service') {
                        
                        about.resources = {
                            'offers': {},
                            'purchases': {},
                            'orders': {},
                            'instances': {}
                        }
                    }
                    
                    console.log(about)
                    return about
                })
            }


            if (type=='service') {

                if (req.UPDATE) {

                    var payload = req.data
                    var handler = payload.handler
                    var name = payload.name
                    var about = payload.about
                    var input = payload.input
                    var output = payload.output

                    var d1 = this.ipfs.put(about)
                    var d2 = this.ipfs.put(input)
                    return $.when( d1, d2 ).done(function ( about, input ) {
                        return service.update(name, about, handler, input, output)
                    })
                }

                if (req.CONFIGURE) {
                    var input = req.data
                    var d1 = this.ipfs.put(input)
                    return $.when( d1 ).done(function ( input ) {
                        return service.setInput(input)
                    })
                }

            }
            
            console.log('unhandled storeitem request ...', req)
        }

        handleUser(req) {
            var self = this
            var userid = req.client.id
            if (req.ABOUT) {

                // userid is adress, not bytes32
                //return this.aboutResource(userid).then(function(about){    
                return self.ethereum.getBalance(userid).then(function(value) {
                    var about = {}
                    about['balance'] = value
                   
                    var registered = about.name    
                    
                    about['options'] = []
                    about['methods'] = {}
                    if (!registered) {
                        about['options'].push('REGISTER')
                        about['methods']['REGISTER'] = {
                            'input': {
                                'params': [
                                    {'name':'name','required':true},
                                    {'name':'url'}
                                ]
                            }
                        }   
                    } else {
                        about['options'].push('UPDATE')
                        about['methods']['UPDATE'] = {
                            'input': {
                                'params': [
                                    {'name':'name','required':true,'value':about['name']},
                                    {'name':'url','value':about.about['url']},
                                    {'name':'logo','value':about.about['logo']},
                                    {'name':'description','value':about.about['description']}
                                ]
                            }
                        }  
                    }

                    about['options'].push('SEND')
                    about['methods']['SEND'] = {
                        'input': {
                            'params': [
                                {'name':'id','required':true},
                                {'name':'amount'}
                            ]
                        }
                    }   
                    
                    about['resources'] = {
                        'subscriptions': {},
                        'purchases': {},
                        'sales': {},
                    }
                    about['ui'] = {
                        'class': 'html',
                        'view': 'row'
                    }
                    return about
                })
            }
            if (req.REGISTER) {
                /*
                var payload = req.data
                var name = payload['name']
                delete payload['name']
                return this.handler.createUser(name,payload)
                */
                var data = req.data
                var name = data['name']
                delete data['name']

                var payload = {
                    'name': name,
                    'about': data
                }
                return this.handler.request('REGISTER','user',payload)
            }
            if (req.UPDATE) {
                /*
                var payload = req.data
                var name = payload['name']
                delete payload['name']
                return this.handler.updateUser(name,payload)
                */
                var data = req.data
                var name = data['name']
                delete data['name']

                var payload = {
                    'name': name,
                    'about': data
                }
                return this.handler.request('UPDATE','user',payload)
            }
            if (req.SEND) {
                /*
                var userid = data['id']
                var value = data['value']
                return this.send(userid,value)
                */
            }

        }


    } 

    window.XioNetworkEthereumHandler = XioNetworkEthereumHandler;

})();



