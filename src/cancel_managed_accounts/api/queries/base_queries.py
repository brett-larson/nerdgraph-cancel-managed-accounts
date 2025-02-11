GET_MANAGED_ACCOUNTS = """
query GetManagedAccounts($isCanceled: Boolean!) {
  actor {
    organization {
      accountManagement {
        managedAccounts(isCanceled: $isCanceled) {
          id
          name
          isCanceled
          regionCode
        }
      }
    }
  }
}
"""