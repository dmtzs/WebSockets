try:
    from app import app
    # from gevent.pywsgi import WSGIServer
except ImportError as e_imp:
    print(f"The following import ERROR occurred in {__file__}: {e_imp}")

if __name__== "__main__":
    try:
        # -----------------Dev mode-----------------
        # run app and print all print from the app
        app.run(host="127.0.0.1", port=5001, debug=False)
        # debug= True for apply changes made into the files without restarting the flask server

        # -----------------Prod mode----------------
        # appServer= WSGIServer(("127.0.0.1", 5000), app)
        # appServer.serve_forever()
    except Exception as e_imp:
        print(f"The following ERROR occurred in {__file__}: {e_imp}")
    finally:
        print("Finishing program")