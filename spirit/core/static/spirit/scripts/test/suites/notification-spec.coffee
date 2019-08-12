describe "notification plugin tests", ->
    responseData = null
    get = null
    tab = null

    isHidden = stModules.utils.isHidden

    beforeEach ->
        fixtures = jasmine.getFixtures()
        fixtures.fixturesPath = 'base/test/fixtures/'
        loadFixtures('notification.html')

        responseData = {
            n: [{
                user: "username",
                action: 1,
                title: "title",
                url: "/foobar/",
                is_read: true
            }]
        }

        get = spyOn(window, 'fetch')
        get.and.callFake( -> {
            then: (func) ->
                data = func({ok: true, json: -> responseData})
                return {
                    then: (func) ->
                        func(data)
                        return {catch: -> {then: (func) -> func()}}
                }
        })

        tab = document.querySelector('.js-tab-notification')
        stModules.notification([tab], {
            notificationUrl: "/foo/",
            notificationListUrl: "/foo/list/",
            mentionTxt: "{user} foo you on {topic}",
            commentTxt: "{user} has bar on {topic}",
            showAll: "foo Show all",
            empty: "foo empty",
            unread: "foo unread"
        })

    it "gets the notifications", ->
        get.calls.reset()

        tab.click()
        expect(get.calls.count()).toEqual(1)
        expect(get.calls.argsFor(0)[0]).toEqual('/foo/')

        # making multiple clicks do nothing
        get.calls.reset()
        tab.click()
        expect(get.calls.count()).toEqual(0)

    it "avoids XSS from topic title", ->
        get.calls.reset()

        responseData = {
            n: [{
                user: "username",  # Username is safe
                action: 1,
                title: '<bad>"bad"</bad>',
                url: "/foobar/",  # URL is safe
                is_read: true
            }]
        }

        tab.click()
        expect(get.calls.count()).toEqual(1)
        expect(document.querySelector('.js-notifications-content').innerHTML).toEqual(
            '<div>username foo you on <a href="/foobar/">&lt;bad&gt;"bad"&lt;/bad&gt;</a></div>' +
            '<div><a href="/foo/list/">foo Show all</a></div>')

    it "shows mention notifications", ->
        get.calls.reset()

        tab.click()
        expect(get.calls.count()).toEqual(1)
        expect(document.querySelector('.js-notifications-content').innerHTML).toEqual(
            '<div>username foo you on <a href="/foobar/">title</a></div>' +
            '<div><a href="/foo/list/">foo Show all</a></div>')

    it "shows comment notifications", ->
        responseData.n[0].action = 2
        tab.click()
        expect(get.calls.count()).toEqual(1)
        expect(document.querySelector('.js-notifications-content').innerHTML).toEqual(
            '<div>username has bar on <a href="/foobar/">title</a></div>' +
            '<div><a href="/foo/list/">foo Show all</a></div>')

    it "marks unread notifications", ->
        responseData.n[0].is_read = false
        tab.click()
        expect(get.calls.count()).toEqual(1)
        expect(document.querySelector('.js-notifications-content').innerHTML).toEqual(
            '<div>username foo you on <a href="/foobar/">title</a> ' +
            '<span class="row-unread">foo unread</span></div>' +
            '<div><a href="/foo/list/">foo Show all</a></div>')

    it "shows an error on server error", ->
        log = spyOn(console, 'log')
        log.and.callFake( -> )

        get.and.callFake( -> {
            then: (func) ->
                try
                    func({ok: false, status: 500, statusText: 'server error'})
                catch err
                    return {
                        then: -> {
                            catch: (func) ->
                                func(err)
                                return {then: (func) -> func()}
                        }
                    }
        })

        tab.click()
        expect(get.calls.count()).toEqual(1)
        expect(document.querySelector('.js-notifications-content').innerHTML).toEqual(
            '<div>error: 500 server error</div>')

    # todo: uncomment once tab.coffee is refactored

    #it "shows tab content and is selected on click", ->
    #    expect(tab.classList.contains("is-selected")).toEqual(false)
    #    expect(isHidden(document.querySelectorAll('.js-notifications-content'))).toEqual(true)
    #
    #    tab.click()
    #    expect(tab.classList.contains("is-selected")).toEqual(true)
    #    expect(isHidden(document.querySelectorAll('.js-notifications-content'))).toEqual(false)

    it "prevents the default click behaviour", ->
        evt = document.createEvent("HTMLEvents")
        evt.initEvent("click", false, true)

        stopPropagation = spyOn(evt, 'stopPropagation')
        preventDefault = spyOn(evt, 'preventDefault')

        tab.dispatchEvent(evt)
        expect(stopPropagation).toHaveBeenCalled()
        expect(preventDefault).toHaveBeenCalled()
