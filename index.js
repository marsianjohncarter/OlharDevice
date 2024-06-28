let parentArr = [
    [
        {
        firstName: "John",
        lastName: "Doe",
        song: "Rock",
        },
        {
        firstName: "Emily",
        lastName: "Jones",
        song: "Rock",
        },
        {
        firstName: "David",
        lastName: "Williams",
        song: "Rock",
        },
    ],
    [
        {
        firstName: "Alice",
        lastName: "Johnson",
        song: "Jazz",
        },
        {
        firstName: "John",
        lastName: "Doe",
        song: "Jazz",
        },
        {
        firstName: "Jane",
        lastName: "Smith",
        song: "Jazz",
        },
    ],
    [
        {
        firstName: "Jennifer",
        lastName: "Miller",
        song: "Pop",
        },
    ],
];

const testArr = [
    [  
        {'test':1},
        {'test2':2},
        {'test3':3}
    ],
    [  
        {'test':1},
        {'test422':2},
        {'test533':3}
    ]
]

for (i in testArr) {
    if (testArr[i + 1]) {
        for (j in testArr[i]) {
            if (testArr[i + 1].find(testArr[i][j])) {
                // return true;
                console.log('true: ' + j);
            } 
        }
        // return false;
        console.log('false');
        
    } else {
        // return false;
        console.log('false');

    }
}






function compareArrays(array1, array2) {
if (!array1 || !array2) {
    return false;
}

const length1 = array1.length;
const length2 = array2.length;

//iterate through each element of array1
for (let i = 0; i < length1; i++) {
    //compare array[i] with each element of array2
    for (let j = 0; j < length2; j++) {
    if (
        array1[i].firstName === array2[j].firstName &&
        array1[i].lastName === array2[j].lastName
    ) {
        console.log("Match found!");
        return true; //A match was found
    }
    }
}
return false; //No match was found in array1
}


function pushMatchingToEnd(parentArray) {
    let length = parentArray.length;
    let i = 0;

    while (i < length) {
        const currentArray = parentArray[i];
        let j = i + 1;

        while (j < length) {
        const nextArray = parentArray[j];

        // Compare the current array to the next array
        if (compareArrays(currentArray, nextArray)) {
            // If they match, push nextArray to the end of parentArray
            parentArray.push(nextArray);
            // Remove nextArray from its current position
            parentArray.splice(j, 1);
            // Decrement length to account for the added element
            length--;
            // Decrement j to stay at the same index in the next iteration
            j--;
        }

        j++;
        }

        // Move to the next array in parentArray
        i++;
    }
}

// pushMatchingToEnd(parentArr);
// console.log(parentArr);