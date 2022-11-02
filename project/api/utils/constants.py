# create class for constants
class JsonConstants:
    connectionId = 'connection_id'
    task = 'task'
    contentType = 'content-type'
    applicationJson = 'application/json'
    success = 'success'
    msg = 'msg'

class ServerResponse:
    serverError = 'Internal server error'
    badRequest = 'Bad Request'
    deleteConnection = 'deleted connection id'
    invalidMobile = 'Mobile is invalid'
    invalidPassword = 'Password is incorrect'
    missingParams = 'Missing paramters'
    connnectionDbError = 'No connection to database'
    server_error_msg = 'Internal server error'

class FieldInvalidResponse:
    InvalidEmail = "Email seems invalid!"
    InvalidMobile = "Mobile number is invalid!"
    InvalidAge = "Age must be between 18-99 Years"
    InvalidPolicyCover = "Amount must be within 25L to 5Cr"
    InvalidNameLength = "Name must be less than 100 characters"
    NoContents = "All parameters must be there!"
    
class HTTPStatusCode:
    # 1xx: HTTP Informational Codes
    Continue = 100
    SwitchingProtocols = 101
    Processing = 102
    Checkpoint = 103
    RequestURITooLong = 122

    # 2xx: HTTP Successful Codes
    OK = 200
    Created = 201
    Accepted = 202
    NonAuthoritativeInformation = 203
    NoContent = 204
    ResetContent = 205
    PartialContent = 206
    MultiStatus = 207
    AlreadyReported = 208
    IMUsed = 226

    # 3xx: HTTP Redirection Codes
    MultipleChoices = 300
    MovedPermanently = 301
    Found = 302
    SeeOther = 303
    NotModified = 304
    UseProxy = 305
    SwitchProxy = 306
    TemporaryRedirect = 307
    PermanentRedirect = 308

    # 4xx: HTTP Client Error Code
    BadRequest = 400
    Unauthorized = 401
    PaymentRequired = 402
    Forbidden = 403
    NotFound = 404
    MethodNotAllowed = 405
    NotAcceptable = 406
    ProxyAuthenticationRequired = 407
    RequestTimeout = 408
    Conflict = 409
    Gone = 410
    LengthRequired = 411
    PreconditionFailed = 412
    RequestEntityTooLarge = 413
    RequestURITooLong = 414
    UnsupportedMediaType = 415
    RequestedRangeNotSatisfiable = 416
    ExpectationFailed = 417
    ImATeapot = 418
    UnprocessableEntity = 422
    Locked = 423
    FailedDependency = 424
    UnorderedCollection = 425
    UpgradeRequired = 426
    PreconditionRequired = 428
    TooManyRequests = 429
    RequestHeaderFieldsTooLarge = 431
    NoResponse = 444
    RetryWith = 449
    BlockedByWindowsParentalControls = 450
    UnavailableForLegalReasons = 451
    ClientClosedRequest = 499

    # 5xx: HTTP Server Error Codes
    InternalServerError = 500
    NotImplemented = 501
    BadGateway = 502
    ServiceUnavailable = 503
    GatewayTimeout = 504
    HTTPVersionNotSupported = 505
    VariantAlsoNegotiates = 506
    InsufficientStorage = 507
    LoopDetected = 508
    BandwidthLimiExceeded = 509
    NotExtended = 510
    NetworkAuthenticationRequired = 511
    NetworkReadTimeoutError = 598
    NetworkConnectTimeoutError = 599